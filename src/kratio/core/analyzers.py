import pandas as pd
from kratio.core.analyzer_interface import Analyzer
from kratio.core.spacy_loader import SpacyModelLoader
from kratio.utils.timing import timed
from kratio.utils.data_utils import normalize_to_dataframe

class WordAnalyzer(Analyzer):
    def __init__(self):
        self.nlp = SpacyModelLoader.get_nlp()

    @timed("analyzing words")
    def analyze(self, text: str) -> pd.DataFrame:
        doc = self.nlp(text)
        words = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct and token.lemma_.strip()]
        word_counts = pd.Series(words).value_counts()
        return normalize_to_dataframe(word_counts, len(words), "Keyword", "Word")

class NounChunkAnalyzer(Analyzer):
    def __init__(self):
        self.nlp = SpacyModelLoader.get_nlp()

    @timed("analyzing noun chunks")
    def analyze(self, text: str) -> pd.DataFrame:
        doc = self.nlp(text)
        noun_chunks = [
            chunk.text.lower()
            for chunk in doc.noun_chunks
            if not chunk.root.is_stop and not chunk.root.is_punct and chunk.text.strip()
        ]
        noun_counts = pd.Series(noun_chunks).value_counts()
        return normalize_to_dataframe(noun_counts, len(noun_chunks), "Noun Chunk", "NounChunk")