from collections import defaultdict
from app.config import client


class AIModel:
    def __init__(self):
        # Bigram storage
        self.bigram = defaultdict(lambda: defaultdict(int))

    # -------- TRAIN BIGRAM --------
    def train_bigram(self, sentences):
        for sentence in sentences:
            words = sentence.lower().split()

            for i in range(len(words) - 1):
                w1 = words[i]
                w2 = words[i + 1]
                self.bigram[w1][w2] += 1

    # -------- BIGRAM PREDICTION --------
    def predict_bigram(self, word):
        candidates = self.bigram.get(word, {})

        sorted_words = sorted(
            candidates.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [w for w, _ in sorted_words]

    # -------- AI PREDICTION --------
    def predict_ai(self, text):
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "user",
                        "content": f"""
                        Suggest exactly 3 different next words for this sentence:
                        '{text}'
                        
                        Rules:
                        - Only return 3 words
                        - No sentences
                        - No explanation
                        - Format: word1, word2, word3
                        """
                    }
                ],
                max_tokens=20
            )

            output = response.choices[0].message.content.strip()

            # Convert string → list
            suggestions = [
                w.strip().lower()
                for w in output.split(",")
                if w.strip()
            ]

            return suggestions[:3]

        except Exception as e:
            print("AI Error:", e)
            return []

    # -------- HYBRID SMART PREDICTION --------
    def smart_predict(self, text, last_word):
        # 1. Try AI
        ai_suggestions = self.predict_ai(text)

        # 2. If AI gives enough suggestions → use it
        if len(ai_suggestions) >= 3:
            return ai_suggestions[:3]

        # 3. Otherwise fallback to bigram
        bigram_suggestions = self.predict_bigram(last_word)

        # 4. Combine both
        combined = []
        seen = set()

        for word in ai_suggestions + bigram_suggestions:
            if word not in seen:
                combined.append(word)
                seen.add(word)

        # 5. Ensure at least 3 suggestions
        fallback_words = ["the", "is", "you", "to", "and"]

        for word in fallback_words:
            if len(combined) >= 3:
                break
            if word not in seen:
                combined.append(word)
                seen.add(word)

        return combined[:3]
