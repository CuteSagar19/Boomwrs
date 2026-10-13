import game

def print_board(guesses, answer):
    for guess in guesses:
        scores = game.score_guess(guess, answer)
        formatted_guess = ""
        for i in range(len(guess)):
            if scores[i] == "green":
                formatted_guess += f"\033[92m{guess[i].upper()}\033[0m "
            elif scores[i] == "orange":
                formatted_guess += f"\033[93m{guess[i].upper()}\033[0m "
            else:
                formatted_guess += f"{guess[i].upper()} "
        print(formatted_guess)
        
def print_keyboard(colors):
    rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    for row in rows:
        formatted_row = ""
        for letter in row:
            color = colors[letter]
            if color == "green":
                formatted_row += f"\033[92m{letter.upper()}\033[0m "
            elif color == "orange":
                formatted_row += f"\033[93m{letter.upper()}\033[0m "
            elif color == "white":
                formatted_row += f"\033[90m{letter.upper()}\033[0m "
            else:
                formatted_row += f"{letter.upper()} "
        print(formatted_row)

def main():
    game.load_words()
    answer = game.pick_word()
    
    if answer == "error":
        print("Error loading words. Did you run make_words.py?")
        return
        
    print("Welcome to Boomwrs CLI!")
    print(f"Guess the {len(answer)}-letter word. You have 6 attempts.")
    
    guesses = []
    
    while len(guesses) < 6:
        print("\n-------------------")
        print_keyboard(game.keyboard_colors(guesses, answer))
        print("-------------------")
        
        guess = input(f"Guess {len(guesses) + 1}/6: ").strip().lower()
        
        if len(guess) != len(answer):
            print(f"Not enough letters. The word is {len(answer)} letters long.")
            continue
            
        if not game.is_real_word(guess):
            print("No such word is present.")
            continue
            
        guesses.append(guess)
        print_board(guesses, answer)
        
        if guess == answer:
            print(f"\nCongratulations! You found the word {answer.upper()} in {len(guesses)} attempts.")
            return
            
    print(f"\nGame over. The word was {answer.upper()}.")

if __name__ == "__main__":
    main()
