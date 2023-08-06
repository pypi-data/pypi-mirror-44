"""
    SQLAlchemy-Rope
    -----------This module provides easy wrapper for thread-local SQLAlchemy session

    :copyright: (c) 2019 by Yamato Nagata.
    :license: MIT.
"""

from .__about__ import __version__
from .session import (SessionJenny, SessionRope)


__all__ = [
    __version__,
    "SessionJenny",
    "SessionRope"
]