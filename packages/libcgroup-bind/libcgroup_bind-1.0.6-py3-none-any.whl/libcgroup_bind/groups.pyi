# coding: UTF-8

from ctypes import Structure, c_bool, c_char_p, c_int, c_int64, c_uint, c_uint64, pointer
from typing import Type, Union

from .init import c_char_pp
from .iterators import c_int_p

try:
    from enum import IntFlag
except ImportError:
    from enum import IntEnum as IntFlag

from . import _CtypesEnum


class DeleteFlag(_CtypesEnum, IntFlag):
    NONE = ...
    IGNORE_MIGRATION = ...
    RECURSIVE = ...
    EMPTY_ONLY = ...


class CGroup(Structure):
    pass


CGroupPointer: Type[pointer[CGroup]]
CGroupDoublePointer: Type[pointer[CGroupPointer]]


class CGroupController(Structure):
    pass


CGroupControllerPointer: Type[pointer[CGroupController]]


# struct cgroup *cgroup_new_cgroup(const char *name);
def cgroup_new_cgroup(name: Union[c_char_p, bytes]) -> CGroupPointer: ...


# struct cgroup_controller *cgroup_add_controller(struct cgroup *cgroup, const char *name);
def cgroup_add_controller(cgroup: CGroupPointer, name: Union[c_char_p, bytes]) -> CGroupControllerPointer: ...


# struct cgroup_controller *cgroup_get_controller(struct cgroup *cgroup, const char *name);
def cgroup_get_controller(cgroup: CGroupPointer, name: Union[c_char_p, bytes]) -> CGroupControllerPointer: ...


# void cgroup_free(struct cgroup **cgroup);
def cgroup_free(cgroup: CGroupDoublePointer) -> None: ...


# void cgroup_free_controllers(struct cgroup *cgroup);
def cgroup_free_controllers(cgroup: CGroupPointer) -> None: ...


# int cgroup_create_cgroup(struct cgroup *cgroup, int ignore_ownership);
def cgroup_create_cgroup(cgroup: CGroupPointer, ignore_ownership: Union[c_int, int]) -> Union[c_int, int]: ...


# int cgroup_create_cgroup_from_parent(struct cgroup *cgroup, int ignore_ownership);
def cgroup_create_cgroup_from_parent(cgroup: CGroupPointer,
                                     ignore_ownership: Union[c_int, int]) -> Union[c_int, int]: ...


# int cgroup_modify_cgroup(struct cgroup *cgroup);
def cgroup_modify_cgroup(cgroup: CGroupPointer) -> Union[c_int, int]: ...


# int cgroup_delete_cgroup(struct cgroup *cgroup, int ignore_migration);
def cgroup_delete_cgroup(cgroup: CGroupPointer, ignore_ownership: Union[c_int, int]) -> Union[c_int, int]: ...


# int cgroup_delete_cgroup_ext(struct cgroup *cgroup, int flags);
def cgroup_delete_cgroup_ext(cgroup: CGroupPointer, flags: DeleteFlag) -> Union[c_int, int]: ...


# int cgroup_get_cgroup(struct cgroup *cgroup);
def cgroup_get_cgroup(cgroup: CGroupPointer) -> Union[c_int, int]: ...


# int cgroup_copy_cgroup(struct cgroup *dst, struct cgroup *src);
def cgroup_copy_cgroup(dst: CGroupPointer, src: CGroupPointer) -> Union[c_int, int]: ...


# int cgroup_compare_cgroup(struct cgroup *cgroup_a, struct cgroup *cgroup_b);
def cgroup_compare_cgroup(cgroup_a: CGroupPointer, cgroup_b: CGroupPointer) -> Union[c_int, int]: ...


# int cgroup_compare_controllers(struct cgroup_controller *cgca, struct cgroup_controller *cgcb);
def cgroup_compare_controllers(cgca: CGroupPointer, cgcb: CGroupPointer) -> Union[c_int, int]: ...


# int cgroup_set_uid_gid(struct cgroup *cgroup, uid_t tasks_uid, gid_t tasks_gid, uid_t control_uid, gid_t control_gid);
def cgroup_set_uid_gid(cgroup: CGroupPointer,
                       tasks_uid: Union[c_uint, int],
                       tasks_gid: Union[c_uint, int],
                       control_uid: Union[c_uint, int],
                       control_gid: Union[c_uint, int]) -> Union[c_int, int]: ...


c_uint_p: Type[pointer[c_uint]]


# int cgroup_get_uid_gid(struct cgroup *cgroup, uid_t *tasks_uid, gid_t *tasks_gid,
#                        uid_t *control_uid, gid_t *control_gid);
def cgroup_get_uid_gid(cgroup: CGroupPointer,
                       tasks_uid: c_uint_p,
                       tasks_gid: c_uint_p,
                       control_uid: c_uint_p,
                       control_gid: c_uint_p) -> Union[c_int, int]: ...


# void cgroup_set_permissions(struct cgroup *cgroup, mode_t control_dperm, mode_t control_fperm, mode_t task_fperm);
def cgroup_set_permissions(cgroup: CGroupPointer,
                           control_dperm: c_uint_p,
                           control_fperm: c_uint_p,
                           task_fperm: c_uint_p) -> None: ...


# int cgroup_add_value_string(struct cgroup_controller *controller, const char *name, const char *value);
def cgroup_add_value_string(controller: CGroupControllerPointer,
                            name: Union[c_char_p, bytes],
                            value: Union[c_char_p, bytes]) -> Union[c_int, int]: ...


# int cgroup_add_value_int64(struct cgroup_controller *controller, const char *name, int64_t value);
def cgroup_add_value_int64(controller: CGroupControllerPointer,
                           name: Union[c_char_p, bytes],
                           value: Union[c_int64, int]) -> Union[c_int, int]: ...


# int cgroup_add_value_uint64(struct cgroup_controller *controller, const char *name, u_int64_t value);
def cgroup_add_value_uint64(controller: CGroupControllerPointer,
                            name: Union[c_char_p, bytes],
                            value: Union[c_uint64, int]) -> Union[c_int, int]: ...


# int cgroup_add_value_bool(struct cgroup_controller *controller, const char *name, bool value);
def cgroup_add_value_bool(controller: CGroupControllerPointer,
                          name: Union[c_char_p, bytes],
                          value: Union[c_bool, bool]) -> Union[c_int, int]: ...


# int cgroup_get_value_string(struct cgroup_controller *controller, const char *name, char **value);
def cgroup_get_value_string(controller: CGroupControllerPointer,
                            name: Union[c_char_p, bytes],
                            value: c_char_pp) -> Union[c_int, int]: ...


c_int64_p: Type[pointer[c_int64]]


# int cgroup_get_value_int64(struct cgroup_controller *controller, const char *name, int64_t *value);
def cgroup_get_value_int64(controller: CGroupControllerPointer,
                           name: Union[c_char_p, bytes],
                           value: c_int64_p) -> Union[c_int, int]: ...


c_uint64_p: Type[pointer[c_uint64]]


# int cgroup_get_value_uint64(struct cgroup_controller *controller, const char *name, u_int64_t *value);
def cgroup_get_value_uint64(controller: CGroupControllerPointer,
                            name: Union[c_char_p, bytes],
                            value: c_uint64_p) -> Union[c_int, int]: ...


c_bool_p: Type[pointer[c_bool]]


# int cgroup_get_value_bool(struct cgroup_controller *controller, const char *name, bool *value);
def cgroup_get_value_bool(controller: CGroupControllerPointer,
                          name: Union[c_char_p, bytes],
                          value: c_bool_p) -> Union[c_int, int]: ...


# int cgroup_set_value_string(struct cgroup_controller *controller, const char *name, const char *value);
def cgroup_set_value_string(controller: CGroupControllerPointer,
                            name: Union[c_char_p, bytes],
                            value: Union[c_char_p, bytes]) -> Union[c_int, int]: ...


# int cgroup_set_value_int64(struct cgroup_controller *controller, const char *name, int64_t value);
def cgroup_set_value_int64(controller: CGroupControllerPointer,
                           name: Union[c_char_p, bytes],
                           value: Union[c_int64, int]) -> Union[c_int, int]: ...


# int cgroup_set_value_uint64(struct cgroup_controller *controller, const char *name, u_int64_t value);
def cgroup_set_value_uint64(controller: CGroupControllerPointer,
                            name: Union[c_char_p, bytes],
                            value: Union[c_uint64, int]) -> Union[c_int, int]: ...


# int cgroup_set_value_bool(struct cgroup_controller *controller, const char *name, bool value);
def cgroup_set_value_bool(controller: CGroupControllerPointer,
                          name: Union[c_char_p, bytes],
                          value: Union[c_bool, bool]) -> Union[c_int, int]: ...


# int cgroup_get_value_name_count(struct cgroup_controller *controller);
def cgroup_get_value_name_count(controller: CGroupControllerPointer) -> Union[c_int, int]: ...


# char *cgroup_get_value_name(struct cgroup_controller *controller, int index);
def cgroup_get_value_name(controller: CGroupControllerPointer, index: Union[c_int, int]) -> Union[c_char_p, bytes]: ...


c_int_pp: Type[pointer[c_int_p]]


# int cgroup_get_procs(char *name, char *controller, pid_t **pids, int *size);
def cgroup_get_procs(name: Union[c_char_p, bytes],
                     controller: Union[c_char_p, bytes],
                     pids: c_int_pp, size: c_int_p) -> Union[c_int, int]: ...


# int cg_chmod_recursive(struct cgroup *cgroup, mode_t dir_mode, int dirm_change, mode_t file_mode, int filem_change);
def cg_chmod_recursive(cgroup: CGroupPointer,
                       dir_mode: Union[c_uint, int],
                       dirm_change: Union[c_int, int],
                       file_mode: Union[c_uint, int],
                       filem_change: Union[c_int, int]) -> Union[c_int, int]: ...

# TODO: undefined
# char *cgroup_get_cgroup_name(struct cgroup *cgroup);
# def cgroup_get_cgroup_name(cgroup: CGroupPointer) -> c_char_p: ...
