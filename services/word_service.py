import nltk
import gensim.downloader as api
import httpx

nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

from nltk.corpus import wordnet
from models.word_model import WordResponse, RelatedWord, Meaning

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"

class WordService:
    def __init__(self):
        print("Loading GloVe model...")
        self.glove_model = api.load("glove-wiki-gigaword-50")
        self.abhishek = "abhishek"
        print("GloVe model loaded!")


    def _get_meanings_from_wordnet(self, word: str) -> list[dict]:
        for pos in [wordnet.NOUN, wordnet.ADJ_SAT, wordnet.ADJ, wordnet.VERB]:
            synsets = wordnet.synsets(word, pos=pos)
            if synsets:
                return [
                    {
                        "definition": s.definition(),
                        "examples": [e for e in s.examples() if word.lower() in e.lower()]
                    }
                    for s in synsets[:3]
                ]
        return []


    def _generate_examples(self, word: str, definition: str) -> list[str]:
        prompt = (
            f'Write exactly 2 short example sentences that use the word "{word}" '
            f'with this meaning: "{definition}". '
            f'Output only the 2 sentences, one per line, no numbering, no extra text.'
        )
        try:
            response = httpx.post(
                OLLAMA_URL,
                json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
                timeout=30,
            )
            response.raise_for_status()
            text = response.json().get("response", "").strip()
            sentences = [s.strip() for s in text.splitlines() if s.strip()]
            return sentences[:2]
        except Exception:
            return []


    def _build_meanings(self, word: str) -> list[Meaning]:
        raw = self._get_meanings_from_wordnet(word)
        meanings = []
        for entry in raw:
            examples = entry["examples"]
            if not examples:
                examples = self._generate_examples(word, entry["definition"])
            meanings.append(Meaning(definition=entry["definition"], examples=examples))
        return meanings


    def get_word_info(self, word: str) -> WordResponse:
        meanings = self._build_meanings(word)
        related_words = self._get_similar_words(word)
        return WordResponse(word=word, meanings=meanings, related_words=related_words)


    def _get_similar_words(self, word: str) -> list[RelatedWord]:
        try:
            similar = self.glove_model.most_similar(word, topn=8)
            return [
                RelatedWord(word=w, similarity=round(score, 4))
                for w, score in similar
            ]
        except KeyError:
            return []


    def judge_practice(self, word: str, sentence: str) -> tuple[bool, str]:
        prompt = (
            f'A student is learning the word "{word}". '
            f'They wrote this sentence: "{sentence}". '
            f'Did they demonstrate understanding of what "{word}" means? '
            f'Be lenient on grammar — focus only on whether the word is used '
            f'with the right meaning in the right context. '
            f'A simple sentence like "I am an epitome of diligence" is correct '
            f'if it shows understanding of the word. '
            f'Reply with a JSON object with exactly two keys: '
            f'"correct" (boolean) and "feedback" (one encouraging sentence). '
            f'Output only the JSON, nothing else.'
        )
        try:
            response = httpx.post(
                OLLAMA_URL,
                json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
                timeout=30,
            )
            response.raise_for_status()
            import json
            data = json.loads(response.json().get("response", "{}"))
            return bool(data.get("correct", False)), str(data.get("feedback", "No feedback."))
        except Exception as e:
            return False, f"Could not evaluate sentence: {e}"
