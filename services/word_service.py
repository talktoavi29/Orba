import nltk
import gensim.downloader as api
import numpy as np

nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

from nltk.corpus import wordnet
from models.word_model import WordResponse, RelatedWord

class WordService:
    def __init__(self):
        print("Loading GloVe Model..")
        self.glove_model = api.load("glove-wiki-gigaword-50")
        print("Glove model loaded!")

    def _get_from_wordnet(self, word: str):
        # Query by POS explicitly so filtering is reliable
        for pos in [wordnet.NOUN, wordnet.ADJ_SAT, wordnet.ADJ, wordnet.VERB]:
            synsets = wordnet.synsets(word, pos=pos)
            if not synsets:
                continue
            definition = synsets[0].definition()
            # Search all synsets of this POS for at least one example
            examples = []
            for synset in synsets:
                if synset.examples():
                    examples = synset.examples()
                    break
            return definition, examples

        return None, []

    def get_word_info(self, word:str):
        definition, examples = self._get_from_wordnet(word)
        related_words = self._get_similar_words(word)

        return WordResponse(
            word = word,
            definition = definition,
            examples = examples,
            related_words = related_words
        )

    def _get_similar_words(self, word: str):
        try:
            similar = self.glove_model.most_similar(word, topn=8)
            return[
                RelatedWord(word=w, similarity=round(score,4))
                for w, score in similar
            ]
        except KeyError:
            return[]