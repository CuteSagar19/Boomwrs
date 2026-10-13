import random

ANSWERS = []
VALID_WORDS = set()

def load_words():
    global ANSWERS, VALID_WORDS
    ANSWERS.clear()
    VALID_WORDS.clear()
    
    try:
        with open('answers.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    ANSWERS.append(line.strip())
                
        with open('valid.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    VALID_WORDS.add(line.strip())
    except FileNotFoundError:
        pass

def pick_word():
    lengths = [2, 3, 4, 5, 6]
    weights = [1, 2, 3, 3, 3]
    chosen_length = random.choices(lengths, weights=weights, k=1)[0]
    
    candidates = []
    for w in ANSWERS:
        if len(w) == chosen_length:
            candidates.append(w)
            
    if not candidates:
        return "error"
    return random.choice(candidates)

def score_guess(guess, answer):
    result = ["white"] * len(guess)
    working_answer = list(answer)
    
    # First pass: look for exact matches (green)
    for i in range(len(guess)):
        if guess[i] == answer[i]:
            result[i] = "green"
            working_answer[i] = None
            
    # Second pass: look for right letter wrong spot (orange)
    for i in range(len(guess)):
        if result[i] != "green":
            if guess[i] in working_answer:
                result[i] = "orange"
                idx = working_answer.index(guess[i])
                working_answer[idx] = None
                
    return result

def is_real_word(guess):
    if guess in VALID_WORDS:
        return True
    if guess.endswith("s") and guess[:-1] in VALID_WORDS:
        return True
    return False

def keyboard_colors(guesses, answer):
    colors = {}
    for i in range(26):
        letter = chr(ord('a') + i)
        colors[letter] = "unused"
        
    for guess in guesses:
        scores = score_guess(guess, answer)
        for i in range(len(guess)):
            letter = guess[i]
            score = scores[i]
            current_color = colors[letter]
            
            if score == "green":
                colors[letter] = "green"
            elif score == "orange" and current_color != "green":
                colors[letter] = "orange"
            elif score == "white" and current_color not in ["green", "orange"]:
                colors[letter] = "white"
                
    return colors


