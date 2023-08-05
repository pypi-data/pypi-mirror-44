# coding: UTF-8

from ctypes import Structure, c_char_p, c_int, c_uint, pointer
from typing import Type, Union

from . import _CtypesEnum
from .groups import CGroupPointer
from .init import c_char_pp

try:
    from enum import IntFlag
except ImportError:
    from enum import IntEnum as IntFlag


class CGFlags(_CtypesEnum, IntFlag):
    USECACHE = ...
    USE_TEMPLATE_CACHE = ...


class DaemonType(_CtypesEnum, IntFlag):
    UNCHANGE_CHILDREN = ...
    CANCEL_UNCHANGE_PROCESS = ...


# int cgroup_attach_task(struct cgroup *cgroup);
def cgroup_attach_task(cgroup: CGroupPointer) -> Union[c_int, int]: ...


# int cgroup_attach_task_pid(struct cgroup *cgroup, pid_t tid);
def cgroup_attach_task_pid(cgroup: CGroupPointer, tid: Union[c_int, int]) -> Union[c_int, int]: ...


# int cgroup_change_cgroup_path(const char *path, pid_t pid, const char *const controllers[]);
def cgroup_change_cgroup_path(path: Union[c_char_p, bytes],
                              pid: Union[c_int, int],
                              controllers: c_char_pp) -> Union[c_int, int]: ...


# int cgroup_get_current_controller_path(pid_t pid, const char *controller, char **current_path);
def cgroup_get_current_controller_path(pid: Union[c_int, int],
                                       controller: Union[c_char_p, bytes],
                                       current_path: c_char_pp) -> Union[c_int, int]: ...


# int cgroup_init_rules_cache(void);
def cgroup_init_rules_cache() -> Union[c_int, int]: ...


# int cgroup_reload_cached_rules(void);
def cgroup_reload_cached_rules() -> Union[c_int, int]: ...


class FILE(Structure):
    pass


FILE_p: Type[pointer[FILE]]


# void cgroup_print_rules_config(FILE *fp);
def cgroup_print_rules_config(fp: FILE_p) -> None: ...


# int cgroup_change_all_cgroups(void);
def cgroup_change_all_cgroups() -> Union[c_int, int]: ...


# int cgroup_change_cgroup_flags(uid_t uid, gid_t gid, const char *procname, pid_t pid, int flags);
def cgroup_change_cgroup_flags(uid: Union[c_uint, int],
                               gid: Union[c_uint, int],
                               procname: Union[c_char_p, bytes],
                               pid: Union[c_int, int],
                               flags: CGFlags) -> Union[c_int, int]: ...


# int cgroup_change_cgroup_uid_gid_flags(uid_t uid, gid_t gid, pid_t pid, int flags);
def cgroup_change_cgroup_uid_gid_flags(uid: Union[c_uint, int],
                                       gid: Union[c_uint, int],
                                       pid: Union[c_int, int],
                                       flags: CGFlags) -> Union[c_int, int]: ...


# int cgroup_change_cgroup_uid_gid(uid_t uid, gid_t gid, pid_t pid);
def cgroup_change_cgroup_uid_gid(uid: Union[c_uint, int],
                                 gid: Union[c_uint, int],
                                 pid: Union[c_int, int]) -> Union[c_int, int]: ...


# int cgroup_register_unchanged_process(pid_t pid, int flags);
def cgroup_register_unchanged_process(pid: Union[c_int, int], flags: DaemonType) -> Union[c_int, int]: ...
