import re
from app.trie import Trie, dfs
from app.ai_model import AIModel

# Matches both English words and Hindi (Devanagari) words
WORD_PATTERN = re.compile(r"[\u0900-\u097F]+|[a-zA-Z']+")

def is_hindi_text(text):
    return bool(re.search(r'[\u0900-\u097F]', text))


class AutocompleteEngine:
    def __init__(self):
        self.trie = Trie()
        self.ai_model = AIModel()

    def train(self, sentences):
        for sentence in sentences:
            words = re.findall(r"[a-zA-Z']+", sentence.lower())
            for word in words:
                self.trie.insert(word)
        self.ai_model.train_bigram(sentences)

    def autocomplete(self, prefix):
        if not prefix:
            return []
        node = self.trie.search_prefix(prefix.lower())
        if not node:
            return []
        results = []
        dfs(node, prefix.lower(), results)
        results.sort(key=lambda x: x[1], reverse=True)
        return [w for w, _ in results[:6]]

    def process_input(self, text, char):
        text += char
        hindi = is_hindi_text(text)
        words = WORD_PATTERN.findall(text.strip())

        if char == " " or char in ".,!?।":
            last = words[-1] if words else ""
            prev = words[-2] if len(words) >= 2 else None
            suggestions = self.ai_model.smart_predict(text, last, prev)
        elif words:
            current_word = words[-1]
            if hindi:
                prev = words[-2] if len(words) >= 2 else None
                suggestions = self.ai_model.smart_predict(text, current_word, prev)
            else:
                suggestions = self.autocomplete(current_word)
                if not suggestions:
                    prev = words[-2] if len(words) >= 2 else None
                    suggestions = self.ai_model.smart_predict(text, current_word, prev)
        else:
            suggestions = []

        return {
            "updated_text": text,
            "suggestions": suggestions[:3]
        }

    def select(self, text, word):
        if text.endswith(" "):
            text += word + " "
        else:
            parts = text.split(" ")
            parts[-1] = word
            text = " ".join(parts) + " "

        words = WORD_PATTERN.findall(text.strip())
        last = words[-1] if words else word
        prev = words[-2] if len(words) >= 2 else None
        suggestions = self.ai_model.smart_predict(text, last, prev)

        return {
            "updated_text": text,
            "suggestions": suggestions[:3]
        }
