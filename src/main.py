with open("data/corrupted_words.txt") as corrupted_word_file:
    corrupted_word_list = corrupted_word_file.read().split("\n")

print(corrupted_word_list)