import json

# Creating classes to correct errored word step by step

## Basic approach: mapping with a hard coded dictionary file, paths and
## other data will be inferred with variables

class BengaliCorrector:
    def __init__(self, dictionary_path):
        self.mappings = {}
        self._load_dictionary(dictionary_path)

    def _load_dictionary(self, path):
        """Loads direct error mappings from JSON."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.mappings = json.load(f)
        except FileNotFoundError:
            print(f"Error: Dictionary file not found at {path}")
            self.mappings = {}

    def correct(self, word):
        """
        Logic: Direct Mapping Only.
        Returns: (Corrected Word, Method)
        """
        word = word.strip()

        # O(1) Lookup, used hashmap(dictionary)
        if word in self.mappings:
            return self.mappings[word], "Direct Map"

        return word, "Unresolved"