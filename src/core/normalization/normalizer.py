import re
from src.core.normalization.synonyms_map import SYNONYMS
from src.utils.text_utils import remove_accents

class Normalizer:
    def __init__(self):
        self.synonyms = SYNONYMS

    def normalize(self, text: str) -> str:
        """
        Main entry point for text normalization.
        """
        if not text:
            return ""
        
        # 1. Basic cleaning (lower, remove accents, special chars)
        text = self._clean_text(text)
        
        # 2. Expand synonyms
        text = self._expand_synonyms(text)
        
        # 3. Deduplicate words
        text = self._dedupe_words(text)
        
        return text.strip()

    def _clean_text(self, text: str) -> str:
        # Lowercase
        text = text.lower()
        
        # Remove accents
        text = remove_accents(text)
        
        # Split alphanumeric (e.g., "mazda3" -> "mazda 3")
        # Look for letter-digit or digit-letter transitions
        text = re.sub(r'([a-z])([0-9])', r'\1 \2', text)
        text = re.sub(r'([0-9])([a-z])', r'\1 \2', text)

        # Remove special characters (keep alphanumeric and spaces)
        # Also keep dots for engine sizes like 1.6, 2.0
        text = re.sub(r'[^a-z0-9\s\.]', ' ', text)
        
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()

    def _expand_synonyms(self, text: str) -> str:
        words = text.split()
        expanded_words = []
        
        for word in words:
            # Check if word is a synonym
            if word in self.synonyms:
                expanded_words.append(self.synonyms[word])
            else:
                expanded_words.append(word)
                
        return " ".join(expanded_words)

    def _dedupe_words(self, text: str) -> str:
        words = text.split()
        seen = set()
        deduped = []
        
        for word in words:
            if word not in seen:
                seen.add(word)
                deduped.append(word)
                
        return " ".join(deduped)

normalizer = Normalizer()
