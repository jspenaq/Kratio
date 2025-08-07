from unittest.mock import MagicMock, patch

import pytest

from src.kratio.core.spacy_loader import SpacyModelLoader


def test_get_nlp_loads_model_successfully():
    # Reset the _nlp instance before each test to ensure isolation
    SpacyModelLoader._nlp = None
    # Arrange
    mock_nlp = MagicMock()
    with patch("spacy.load", return_value=mock_nlp) as mock_spacy_load:
        # Act
        nlp_instance = SpacyModelLoader.get_nlp()

        # Assert
        mock_spacy_load.assert_called_once_with(SpacyModelLoader._model_name)
        assert nlp_instance == mock_nlp
        assert SpacyModelLoader._nlp == mock_nlp


def test_get_nlp_downloads_and_loads_on_oserror():
    # Reset the _nlp instance before each test to ensure isolation
    SpacyModelLoader._nlp = None
    # Arrange
    mock_nlp = MagicMock()
    # Simulate OSError on first load, then successful load on second attempt
    with (
        patch("spacy.load", side_effect=[OSError, mock_nlp]) as mock_spacy_load,
        patch("src.kratio.core.spacy_loader.download") as mock_spacy_download,
        patch("loguru.logger.info") as mock_logger_info,
    ):
        # Act
        nlp_instance = SpacyModelLoader.get_nlp()

        # Assert
        assert mock_spacy_load.call_count == 2
        mock_spacy_load.assert_called_with(SpacyModelLoader._model_name)
        mock_spacy_download.assert_called_once_with(SpacyModelLoader._model_name)
        assert nlp_instance == mock_nlp
        assert SpacyModelLoader._nlp == mock_nlp
        mock_logger_info.assert_any_call(
            f"spaCy model '{SpacyModelLoader._model_name}' not found. Attempting to download...",
        )
        mock_logger_info.assert_any_call(
            f"Successfully downloaded and loaded spaCy model '{SpacyModelLoader._model_name}'.",
        )


def test_get_nlp_exits_on_download_failure():
    # Reset the _nlp instance before each test to ensure isolation
    SpacyModelLoader._nlp = None
    # Arrange
    with (
        patch("spacy.load", side_effect=OSError) as mock_spacy_load,
        patch("src.kratio.core.spacy_loader.download", side_effect=Exception("Download failed")) as mock_spacy_download,
        patch("loguru.logger.exception") as mock_logger_exception,
    ):
        # Act
        with pytest.raises(SystemExit) as excinfo:
            SpacyModelLoader.get_nlp()

        # Assert
        assert excinfo.value.code == 1
        mock_spacy_load.assert_called_once_with(SpacyModelLoader._model_name)
        mock_spacy_download.assert_called_once_with(SpacyModelLoader._model_name)
        mock_logger_exception.assert_called_once()
        assert SpacyModelLoader._nlp is None  # Ensure _nlp remains None on failure
