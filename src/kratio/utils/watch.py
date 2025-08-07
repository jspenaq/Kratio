"""
File system monitoring module for Kratio watch mode.
Uses watchdog to monitor files and directories for changes.
"""

import time
from collections.abc import Callable
from pathlib import Path

from loguru import logger
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from kratio.constants import SUPPORTED_EXTENSIONS
from kratio.io.file_handler import is_directory


class KratioEventHandler(FileSystemEventHandler):
    """
    Custom event handler for Kratio watch mode.
    Filters events based on supported file extensions and triggers re-analysis.
    """

    def __init__(
        self,
        callback: Callable[[Path], None],
        supported_extensions: list[str] = SUPPORTED_EXTENSIONS,
        target_path: str | Path | None = None,
    ) -> None:
        """
        Initialize the event handler.

        Args:
            callback: Function to call when a relevant file change is detected
            supported_extensions: List of file extensions to monitor
            target_path: Specific file to monitor (if not a directory)
        """
        self.callback = callback
        self.supported_extensions = supported_extensions
        self.target_path = Path(target_path) if target_path else None
        self.last_processed_time = 0
        self.debounce_seconds = 0.1  # Reduced debounce time to be more responsive
        logger.debug(f"Initialized event handler with target_path: {self.target_path}")

    def on_modified(self, event: FileSystemEvent) -> None:
        """
        Called when a file or directory is modified.
        Filters events and calls the callback if relevant.
        """
        if event.is_directory:
            return

        # Debounce to avoid multiple rapid triggers
        current_time = time.time()
        if current_time - self.last_processed_time < self.debounce_seconds:
            return

        # Get the path of the modified file
        file_path = Path(str(event.src_path))
        logger.debug(f"Modified event for: {file_path}")

        # If we're watching a specific file, only process events for that file
        if self.target_path:
            target_abs = self.target_path.absolute()
            file_abs = file_path.absolute()
            logger.debug(f"Comparing target: {target_abs} with file: {file_abs}")
            if target_abs != file_abs:
                logger.debug(f"Ignoring event for non-target file: {file_path}")
                return

        # Check if the file has a supported extension
        if file_path.suffix in self.supported_extensions:
            logger.info(f"Change detected in {file_path}")
            self.last_processed_time = current_time
            self.callback(file_path)
        else:
            logger.debug(f"Ignoring file with unsupported extension: {file_path.suffix}")

    def on_moved(self, event: FileSystemEvent) -> None:
        """
        Called when a file or directory is moved/renamed.
        This is important because some editors save files by creating a new one and moving it.
        """
        if event.is_directory:
            return

        # Debounce to avoid multiple rapid triggers
        current_time = time.time()
        if current_time - self.last_processed_time < self.debounce_seconds:
            return

        # Get the destination path
        dest_path = Path(str(event.dest_path)) if hasattr(event, "dest_path") else None
        if not dest_path:
            return

        logger.debug(f"Move event detected: {event.src_path} -> {dest_path}")

        # If we're watching a specific file, only process events for that file
        if self.target_path:
            target_abs = self.target_path.absolute()
            dest_abs = dest_path.absolute()
            if target_abs != dest_abs:
                return

        # Check if the file has a supported extension
        if dest_path.suffix in self.supported_extensions:
            logger.info(f"File moved/renamed to {dest_path}")
            self.last_processed_time = current_time
            self.callback(dest_path)

    def on_created(self, event: FileSystemEvent) -> None:
        """
        Called when a file or directory is created.
        Only relevant when watching a directory.
        """
        if event.is_directory:
            return

        # Get the path of the created file
        file_path = Path(str(event.src_path))
        logger.debug(f"Created event for: {file_path}")

        # If we're watching a specific file, check if this is a new version of it
        # (Some editors create new files instead of modifying existing ones)
        if self.target_path:
            target_abs = self.target_path.absolute()
            file_abs = file_path.absolute()
            if target_abs != file_abs:
                logger.debug(f"Created event for non-target file: {file_path}")
                return

        # Check if the file has a supported extension
        if file_path.suffix in self.supported_extensions:
            logger.info(f"New file detected: {file_path}")
            self.last_processed_time = time.time()
            self.callback(file_path)
        else:
            logger.debug(f"Ignoring created file with unsupported extension: {file_path.suffix}")


class FileWatcher:
    """
    Manages file system monitoring for Kratio watch mode.
    """

    def __init__(self) -> None:
        """Initialize the file watcher."""
        self.observer = None
        self.handler = None
        self.watching = False

    def start_watching(
        self,
        path: str | Path,
        callback: Callable[[Path], None],
        supported_extensions: list[str] | None = None,
    ) -> None:
        """
        Start watching a file or directory for changes.

        Args:
            path: Path to the file or directory to watch
            callback: Function to call when a relevant file change is detected
            supported_extensions: List of file extensions to monitor (defaults to SUPPORTED_EXTENSIONS)
        """
        if self.watching:
            self.stop_watching()

        path_obj = Path(path)
        if not path_obj.exists():
            raise FileNotFoundError(f"Path does not exist: {path}")

        # Determine if we're watching a file or directory
        is_dir = is_directory(str(path))
        watch_path = path_obj if is_dir else path_obj.parent
        target_file = None if is_dir else path_obj

        # Create the event handler
        extensions = supported_extensions or SUPPORTED_EXTENSIONS
        self.handler = KratioEventHandler(callback, extensions, target_file if target_file else None)

        # Create and start the observer
        self.observer = Observer()
        self.observer.schedule(self.handler, str(watch_path), recursive=is_dir)
        self.observer.start()
        self.watching = True

        logger.info(f"Watching {'directory' if is_dir else 'file'}: {path}")
        if not is_dir:
            logger.info(f"Target file absolute path: {path_obj.absolute()}")
        logger.info("Press Ctrl+C to stop watching")

    def stop_watching(self) -> None:
        """Stop watching and clean up resources."""
        if self.observer and self.watching:
            self.observer.stop()
            self.observer.join()
            self.watching = False
            logger.info("Stopped watching")

    def __del__(self) -> None:
        """Ensure resources are cleaned up when the object is destroyed."""
        self.stop_watching()
