import spacy
from loguru import logger
from spacy.cli.download import download


class SpacyModelLoader:
    _nlp = None
    _model_name = "en_core_web_sm"

    @classmethod
    def get_nlp(cls) -> spacy.language.Language:
        if cls._nlp is None:
            try:
                cls._nlp = spacy.load(cls._model_name)
            except OSError:
                logger.info(f"spaCy model '{cls._model_name}' not found. Attempting to download...")
                try:
                    download(cls._model_name)
                    cls._nlp = spacy.load(cls._model_name)
                    logger.info(f"Successfully downloaded and loaded spaCy model '{cls._model_name}'.")
                except Exception:
                    logger.exception(
                        f"Failed to download or load spaCy model '{cls._model_name}'. "
                        "Please ensure you have an active internet connection or run "
                        f"'python -m spacy download {cls._model_name}' manually.",
                    )
                    exit(1)
        return cls._nlp
