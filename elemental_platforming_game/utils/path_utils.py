"""
Utilities for working with paths.
"""
import os.path


def get_resource_file_path(file_path: str) -> str:
    """Returns the full path for the given file held in this package."""
    return os.path.join(os.path.dirname(__file__), '..', file_path)
