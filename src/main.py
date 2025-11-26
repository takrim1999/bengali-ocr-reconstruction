import os
import sys

# All inputs are taken from files, checking the availability
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.corrector import BengaliCorrector

def main():
    # Dynamic path resolution
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ## Putting all problematic words here
    input_path = os.path.join(base_dir, 'data', 'corrupted_words.txt')
    ## Direct mapping dictionary
    dict_path = os.path.join(base_dir, 'data', 'dictionary.json')

    # Initializing a self-made corrector object
    corrector = BengaliCorrector(dict_path)

    print(f"{'Original':<15} | {'Corrected':<15} | {'Method':<15}")
    print("-" * 50)

    # Processing
    if os.path.exists(input_path):
        with open(input_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for line in lines:
            word = line.strip()
            if not word:
                continue

            corrected, method = corrector.correct(word)
            ## Trying to look it structured but without make it variable, the structure will fail
            ## for sure, still distinguishable
            print(f"{word:<15} | {corrected:<15} | {method:<15}")
    else:
        print(f"Error: Input file not found at {input_path}")

if __name__ == "__main__":
    main()