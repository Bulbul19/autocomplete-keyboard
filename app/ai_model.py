from collections import defaultdict
import re

HINDI_RANGE = re.compile(r'[\u0900-\u097F]')

def is_hindi(text):
    return bool(HINDI_RANGE.search(text))


class AIModel:
    def __init__(self):
        self.bigram = defaultdict(lambda: defaultdict(int))
        self.trigram = defaultdict(lambda: defaultdict(int))

    def train_bigram(self, sentences):
        for sentence in sentences:
            words = re.findall(r"[a-zA-Z']+", sentence.lower())
            for i in range(len(words) - 1):
                self.bigram[words[i]][words[i + 1]] += 1
            for i in range(len(words) - 2):
                key = f"{words[i]} {words[i+1]}"
                self.trigram[key][words[i + 2]] += 1

    def predict_bigram(self, word):
        candidates = self.bigram.get(word.lower(), {})
        sorted_words = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
        return [w for w, _ in sorted_words[:5]]

    def predict_trigram(self, prev_word, curr_word):
        key = f"{prev_word.lower()} {curr_word.lower()}"
        candidates = self.trigram.get(key, {})
        sorted_words = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
        return [w for w, _ in sorted_words[:5]]

    def predict_ai(self, text):
        """Uses Groq API for fast contextual prediction. Supports Hindi and English."""
        try:
            from app.config import client
            hindi = is_hindi(text)

            if hindi:
                system_prompt = (
                    "आप एक हिंदी कीबोर्ड ऑटोकम्पलीट इंजन हैं। "
                    "दिए गए वाक्य के बाद आने वाले 3 सबसे सही हिंदी शब्द दें। "
                    "सिर्फ 3 शब्द, comma से अलग। कोई explanation नहीं। "
                    "उदाहरण: पानी, खाना, घर"
                )
                user_msg = f"वाक्य: '{text.strip()}'"
            else:
                system_prompt = (
                    "You are a keyboard autocomplete engine. "
                    "Given a partial sentence, reply ONLY with exactly 3 comma-separated "
                    "next-word suggestions. No explanation, no punctuation at end. "
                    "Example: morning, afternoon, evening"
                )
                user_msg = f"Sentence: '{text.strip()}'"

            response = client.chat.completions.create(
                model="llama3-8b-8192",
                max_tokens=40,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_msg}
                ]
            )
            raw = response.choices[0].message.content.strip()
            print(f"🤖 Groq raw response: {raw}")

            suggestions = [w.strip() for w in raw.split(",")]

            if hindi:
                # Keep only words that have Devanagari characters
                clean = [s.split()[0] for s in suggestions if s.strip() and is_hindi(s)]
                print(f"✅ Hindi suggestions: {clean}")
                return clean[:3]
            else:
                clean = [s.lower().split()[0] for s in suggestions if s.strip() and s.replace(' ','').isalpha()]
                print(f"✅ English suggestions: {clean}")
                return clean[:3]

        except Exception as e:
            print(f"❌ Groq error: {e}")
            return []

    def smart_predict(self, text, last_word, prev_word=None):
        hindi = is_hindi(text)

        # Always try Groq AI first
        ai = self.predict_ai(text)
        if ai:
            return ai

        # Hindi fallback — common Hindi words
        if hindi:
            return ['है', 'और', 'का']

        # English: try trigram then bigram
        if prev_word:
            tri = self.predict_trigram(prev_word, last_word)
            if tri:
                return tri[:3]

        bi = self.predict_bigram(last_word)
        if bi:
            return bi[:3]

        return ["the", "is", "you"]
