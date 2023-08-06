"""
Utilities for use with remote processes.
"""

__all__ = [
    'ChangeDirectory',
]


class ChangeDirectory(object):

    """
    Context manager for temporarily changing current working directory in the
    context of the given ``os`` module.

    :param str path: new path name
    :param _os: module with ``getcwd`` and ``chdir`` functions
    """

    def __init__(self, path, _os):
        self._os = _os
        # Contrary to common implementations of a similar context manager,
        # we change the path immediately in the constructor. That enables
        # this utility to be used without any 'with' statement:
        if path:
            self._restore = _os.getcwd()
            _os.chdir(path)
        else:
            self._restore = None

    def __enter__(self):
        """Enter 'with' context."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit 'with' context and restore old path."""
        if self._restore:
            self._os.chdir(self._restore)
