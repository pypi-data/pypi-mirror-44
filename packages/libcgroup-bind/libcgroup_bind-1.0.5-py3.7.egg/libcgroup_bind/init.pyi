# coding: UTF-8

from ctypes import c_char_p, c_int, pointer
from typing import Type, Union


def cgroup_init() -> Union[c_int, int]: ...


c_char_pp: Type[pointer[c_char_p]]


def cgroup_get_subsys_mount_point(controller: Union[c_char_p, bytes], mount_point: c_char_pp) -> Union[c_int, int]: ...
