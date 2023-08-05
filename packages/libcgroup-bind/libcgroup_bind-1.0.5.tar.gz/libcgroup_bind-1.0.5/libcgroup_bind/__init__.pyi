# coding: UTF-8

from ctypes import CDLL

_libcgroup: CDLL


# Define the types we need.
class _CtypesEnum:
    """A ctypes-compatible IntEnum superclass."""

    @classmethod
    def from_param(cls, obj) -> int: ...
