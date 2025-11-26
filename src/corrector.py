import json
import difflib
import unicodedata


class BengaliCorrector:
    def __init__(self, dictionary_path):
        self.mappings = {}
        self.vocabulary = []
        self._load_dictionary(dictionary_path)

    def _normalize(self, text):
        """
        Unicode Normalization:
        Handles joiners and standardizes Bengali characters (NFKC).
        """
        if not text: return ""
        text = unicodedata.normalize("NFKC", text.strip())
        text = text.replace("\u200d", "").replace("\u200c", "")
        return text

    def _load_dictionary(self, path):
        """Loads direct error mappings and valid vocabulary from JSON and normalizes them."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "direct_mappings" in data:
                    self.mappings = {
                        self._normalize(k): self._normalize(v)
                        for k, v in data["direct_mappings"].items()
                    }
                    self.vocabulary = [
                        self._normalize(w)
                        for w in data.get("valid_vocabulary", [])
                    ]
                else:
                    # Legacy format support
                    self.mappings = {
                        self._normalize(k): self._normalize(v)
                        for k, v in data.items()
                    }
                    self.vocabulary = list(self.mappings.values())

        except FileNotFoundError:
            print(f"Error: Dictionary file not found at {path}")
            self.mappings = {}
            self.vocabulary = []

    def _predict_with_llm(self, word):
        """Prototype: Mock LLM prediction."""
        return f"UNCERTAIN: {word}", "LLM Check"

    def correct(self, word):
        """
        Enhanced Pipeline:
        1. Normalize Input
        2. Direct Mapping (O(1))
        3. Vocabulary Check (O(1))
        4. Space Collapsing (Heuristic)
        5. Fuzzy Match (Levenshtein)
        6. LLM Fallback
        """
        # 1. Normalize
        word_norm = self._normalize(word)
        if not word_norm: return None, "Empty"

        # 2. Direct Lookup
        if word_norm in self.mappings:
            return self.mappings[word_norm], "Direct Map"

        # 3. Validity Check
        if word_norm in self.vocabulary:
            return word_norm, "Valid"

        # 4. Space Collapsing
        collapsed_word = word_norm.replace(" ", "")
        if collapsed_word in self.vocabulary:
            return collapsed_word, "Space Fix"

        if collapsed_word in self.mappings:
            return self.mappings[collapsed_word], "Space+Map"

        # 5. Fuzzy Matching
        matches = difflib.get_close_matches(collapsed_word, self.vocabulary, n=1, cutoff=0.8)
        if matches:
            return matches[0], "Fuzzy Match"

        # 6. LLM Fallback
        return self._predict_with_llm(word_norm)