# coding: UTF-8

from ctypes import Structure, c_char_p, c_int, c_short, c_void_p, pointer
from dataclasses import dataclass
from enum import IntEnum
from typing import Type, Union

from . import _CtypesEnum


class WalkType(_CtypesEnum, IntEnum):
    PRE_DIR = ...
    POST_DIR = ...


class FileType(_CtypesEnum, IntEnum):
    FILE = ...
    DIR = ...
    OTHER = ...


@dataclass
class FileInfo(Structure):
    type: FileType = ...
    path: Union[c_char_p, bytes] = ...
    parent: Union[c_char_p, bytes] = ...
    full_path: Union[c_char_p, bytes] = ...
    depth: Union[c_short, int] = ...


c_void_pp: Type[pointer[c_void_p]]
c_int_p: Type[pointer[c_int]]
FileInfoPointer: Type[pointer[FileInfo]]


# int cgroup_walk_tree_begin(const char *controller, const char *base_path, int depth,
#                            void **handle, struct cgroup_file_info *info, int *base_level);
def cgroup_walk_tree_begin(controller: Union[c_char_p, bytes],
                           base_path: Union[c_char_p, bytes],
                           depth: Union[c_int, int],
                           handle: c_void_pp,
                           info: FileInfoPointer,
                           base_level: c_int_p) -> Union[c_int, int]: ...


# int cgroup_walk_tree_next(int depth, void **handle, struct cgroup_file_info *info, int base_level);
def cgroup_walk_tree_next(depth: Union[c_int, int],
                          handle: c_void_pp,
                          info: FileInfoPointer,
                          base_level: Union[c_int, int]) -> Union[c_int, int]: ...


# int cgroup_walk_tree_end(void **handle);
def cgroup_walk_tree_end(handle: c_void_pp) -> Union[c_int, int]: ...


# int cgroup_walk_tree_set_flags(void **handle, int flags);
def cgroup_walk_tree_set_flags(handle: c_void_pp, flags: WalkType) -> Union[c_int, int]: ...


# int cgroup_read_value_begin(const char *controller, const char *path,
#                             char *name, void **handle, char *buffer, int max);
def cgroup_read_value_begin(controller: Union[c_char_p, bytes],
                            path: Union[c_char_p, bytes],
                            name: Union[c_char_p, bytes],
                            handle: c_void_pp,
                            buffer: Union[c_char_p, bytes],
                            max: Union[c_int, int]) -> Union[c_int, int]: ...


# int cgroup_read_value_next(void **handle, char *buffer, int max);
def cgroup_read_value_next(handle: c_void_pp,
                           buffer: Union[c_char_p, bytes],
                           max: Union[c_int, int]) -> Union[c_int, int]: ...


# int cgroup_read_value_end(void **handle);
def cgroup_read_value_end(handle: c_void_pp) -> Union[c_int, int]: ...


@dataclass
class Stat(Structure):
    name: Union[c_char_p, bytes] = ...
    value: Union[c_char_p, bytes] = ...


StatPointer: Type[pointer[Stat]]


# int cgroup_read_stats_begin(const char *controller, const char *path, void **handle, struct cgroup_stat *stat);
def cgroup_read_stats_begin(controller: Union[c_char_p, bytes],
                            path: Union[c_char_p, bytes],
                            handle: c_void_pp,
                            stat: StatPointer) -> Union[c_int, int]: ...


# int cgroup_read_stats_next(void **handle, struct cgroup_stat *stat);
def cgroup_read_stats_next(handle: c_void_pp, stat: StatPointer) -> Union[c_int, int]: ...


# int cgroup_read_stats_end(void **handle);
def cgroup_read_stats_end(handle: c_void_pp) -> Union[c_int, int]: ...


# int cgroup_get_task_begin(const char *cgroup, const char *controller, void **handle, pid_t *pid);
def cgroup_get_task_begin(cgroup: Union[c_char_p, bytes],
                          controller: Union[c_char_p, bytes],
                          handle: c_void_pp,
                          pid: c_int_p) -> Union[c_int, int]: ...


# int cgroup_get_task_next(void **handle, pid_t *pid);
def cgroup_get_task_next(handle: c_void_pp, pid: c_int_p) -> Union[c_int, int]: ...


# int cgroup_get_task_end(void **handle);
def cgroup_get_task_end(handle: c_void_pp) -> Union[c_int, int]: ...


@dataclass
class MountPoint(Structure):
    name: Union[c_char_p, bytes] = ...
    path: Union[c_char_p, bytes] = ...


MountPointPointer: Type[pointer[MountPoint]]


# int cgroup_get_controller_begin(void **handle, struct cgroup_mount_point *info);
def cgroup_get_controller_begin(handle: c_void_pp, info: MountPointPointer) -> Union[c_int, int]: ...


# int cgroup_get_controller_next(void **handle, struct cgroup_mount_point *info);
def cgroup_get_controller_next(handle: c_void_pp, info: MountPointPointer) -> Union[c_int, int]: ...


# int cgroup_get_controller_end(void **handle);
def cgroup_get_controller_end(handle: c_void_pp) -> Union[c_int, int]: ...


@dataclass
class ControllerData(Structure):
    name: Union[c_char_p, bytes] = ...
    hierarchy: Union[c_int, int] = ...
    num_cgroups: Union[c_int, int] = ...
    enabled: Union[c_int, int] = ...


ControllerDataPointer: Type[pointer[ControllerData]]


# int cgroup_get_all_controller_begin(void **handle, struct controller_data *info);
def cgroup_get_all_controller_begin(handle: c_void_pp, info: ControllerDataPointer) -> Union[c_int, int]: ...


# int cgroup_get_all_controller_next(void **handle, struct controller_data *info);
def cgroup_get_all_controller_next(handle: c_void_pp, info: ControllerDataPointer) -> Union[c_int, int]: ...


# int cgroup_get_all_controller_end(void **handle);
def cgroup_get_all_controller_end(handle: c_void_pp) -> Union[c_int, int]: ...


# int cgroup_get_subsys_mount_point_begin(const char *controller, void **handle, char *path);
def cgroup_get_subsys_mount_point_begin(controller: Union[c_char_p, bytes],
                                        handle: c_void_pp,
                                        path: Union[c_char_p, bytes]) -> Union[c_int, int]: ...


# int cgroup_get_subsys_mount_point_next(void **handle, char *path);
def cgroup_get_subsys_mount_point_next(handle: c_void_pp, path: Union[c_char_p, bytes]) -> Union[c_int, int]: ...


# int cgroup_get_subsys_mount_point_end(void **handle);
def cgroup_get_subsys_mount_point_end(handle: c_void_pp) -> Union[c_int, int]: ...
