import json
import difflib  # Added for Sprint 2: Fuzzy matching logic


# Creating classes to correct errored word step by step
# Sprint 1: Basic mapping
# Sprint 2: Advanced fuzzy matching

class BengaliCorrector:
    def __init__(self, dictionary_path):
        self.mappings = {}
        self.vocabulary = []  # storing vocabulary to fuzzyfy
        self._load_dictionary(dictionary_path)

    def _load_dictionary(self, path):
        """
        Loads direct error mappings and valid vocabulary from JSON.
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # Check if data is the old flat format or new structured format
                if "direct_mappings" in data:
                    self.mappings = data["direct_mappings"]
                    self.vocabulary = data.get("valid_vocabulary", [])
                else:
                    # Fallback for legacy format (Sprint 1 compatibility)
                    self.mappings = data
                    self.vocabulary = list(data.values())  # Infer vocabulary if missing

        except FileNotFoundError:
            print(f"Error: Dictionary file not found at {path}")
            self.mappings = {}
            self.vocabulary = []

    def correct(self, word):
        """
        Logic:
        1. Direct Mapping (O(1)) - Specific known errors
        2. Vocabulary Check (O(1)) - Already correct words
        3. Fuzzy Match (Levenshtein) - Typos not in the map

        Returns: (Corrected Word, Method)
        """
        word = word.strip()
        if not word: return None, "Empty"

        # Step 1: O(1) Lookup (Sprint 1 Feature)
        if word in self.mappings:
            return self.mappings[word], "Direct Map"

        # Step 2: Check if the word is already valid (New Feature)
        if word in self.vocabulary:
            return word, "Valid"

        # Step 3: Fuzzy Matching (Sprint 2 Feature - Advanced)
        # Uses Levenshtein distance to find the closest vocabulary match
        # cutoff=0.6 ensures we don't match completely random words
        matches = difflib.get_close_matches(word, self.vocabulary, n=1, cutoff=0.6)

        if matches:
            return matches[0], "Fuzzy Match"

        return word, "Unresolved"