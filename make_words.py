import string
import random
import nltk
from wordfreq import top_n_list, zipf_frequency

# validating words corpus download has been proper
nltk.download('words', quiet=True)
from nltk.corpus import words

def main():
    nltk_words = set(w.lower() for w in words.words())
    
    # Get top 30,000 words
    top_words = top_n_list('en', 30000)
    
    answers = []
    
    # Process answers
    for word in top_words:
        if len(word) >= 2 and len(word) <= 6:
            if all(c in string.ascii_lowercase for c in word):
                if word in nltk_words:
                    score = zipf_frequency(word, 'en')
                    # Zipf threshold
                    # If two-letter words feel too few, lower it slightly for length 2 only
                    threshold = 3.5
                    if len(word) == 2:
                        threshold = 3.0
                    
                    if score >= threshold:
                        answers.append(word)
    
    # Process valid words
    valid_words = set(answers)
    for word in nltk_words:
        if len(word) >= 2 and len(word) <= 6 and all(c in string.ascii_lowercase for c in word):
            valid_words.add(word)
    
    # Save answers
    with open('answers.txt', 'w', encoding='utf-8') as f:
        for word in sorted(answers):
            f.write(word + '\n')
            
    # Save valid words
    with open('valid.txt', 'w', encoding='utf-8') as f:
        for word in sorted(valid_words):
            f.write(word + '\n')
            
    # Print 40 random words per length
    answers_by_length = {2: [], 3: [], 4: [], 5: [], 6: []}
    for word in answers:
        answers_by_length[len(word)].append(word)
        
    for length in range(2, 7):
        print(f"--- Length {length} (Total: {len(answers_by_length[length])}) ---")
        pool = answers_by_length[length]
        sample_size = min(40, len(pool))
        if sample_size > 0:
            sample = random.sample(pool, sample_size)
            print(", ".join(sample))
        print()

if __name__ == "__main__":
    main()
