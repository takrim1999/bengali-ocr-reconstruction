import json
import difflib

# Sprint 3 Update: Added LLM Prototype for fallback handling

class BengaliCorrector:
    def __init__(self, dictionary_path):
        self.mappings = {}
        self.vocabulary = []
        self._load_dictionary(dictionary_path)

    def _load_dictionary(self, path):
        """Loads direct error mappings and valid vocabulary from JSON."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if "direct_mappings" in data:
                    self.mappings = data["direct_mappings"]
                    self.vocabulary = data.get("valid_vocabulary", [])
                else:
                    self.mappings = data
                    self.vocabulary = list(data.values())
        except FileNotFoundError:
            print(f"Error: Dictionary file not found at {path}")
            self.mappings = {}
            self.vocabulary = []

    def _predict_with_llm(self, word):
        """
        Prototype: Simulates an API call to an LLM (e.g., OpenAI/Gemini).
        Since we cannot use external APIs per constraints, this mocks the response.
        """
        # In production: response = openai.Completion.create(prompt=f"Correct Bengali OCR: {word}")
        # For Assessment: returning the word tagged to demonstrate flow
        return f"{word}?", "LLM Check"

    def correct(self, word):
        """
        Full Pipeline:
        1. Direct Mapping (O(1)) - Specific known errors
        2. Vocabulary Check (O(1)) - Already correct words
        3. Fuzzy Match (Levenshtein) - Typos (distance-based)
        4. LLM Fallback (API) - Contextual prediction for unknowns
        """
        word = word.strip()
        if not word: return None, "Empty"

        # 1. Direct Lookup
        if word in self.mappings:
            return self.mappings[word], "Direct Map"

        # 2. Validity Check
        if word in self.vocabulary:
            return word, "Valid"

        # 3. Fuzzy Matching
        matches = difflib.get_close_matches(word, self.vocabulary, n=1, cutoff=0.6)
        if matches:
            return matches[0], "Fuzzy Match"

        # 4. LLM Fallback (Sprint 3 Feature)
        # If the word is truly unknown and fails fuzzy match, ask the AI.
        return self._predict_with_llm(word)