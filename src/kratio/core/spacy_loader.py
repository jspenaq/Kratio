import spacy
from loguru import logger

class SpacyModelLoader:
    _nlp = None

    @classmethod
    def get_nlp(cls):
        if cls._nlp is None:
            try:
                cls._nlp = spacy.load("en_core_web_sm")
            except OSError:
                logger.exception(
                    "Downloading spaCy model 'en_core_web_sm' failed. "
                    "Please run 'python -m spacy download en_core_web_sm' to download it manually.",
                )
                exit(1)
        return cls._nlp