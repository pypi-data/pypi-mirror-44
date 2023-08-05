# coding: UTF-8

from ctypes import c_char_p, c_int
from typing import Union

from .groups import CGroupPointer, DeleteFlag


# int cgroup_config_load_config(const char *pathname);
def cgroup_config_load_config(pathname: Union[c_char_p, bytes]) -> Union[c_int, int]: ...


# int cgroup_unload_cgroups(void);
def cgroup_unload_cgroups() -> Union[c_int, int]: ...


# int cgroup_config_unload_config(const char *pathname, int flags);
def cgroup_config_unload_config(pathname: Union[c_char_p, bytes], flags: DeleteFlag) -> Union[c_int, int]: ...


# int cgroup_config_set_default(struct cgroup *new_default);
def cgroup_config_set_default(new_default: CGroupPointer) -> Union[c_int, int]: ...


# int cgroup_init_templates_cache(char *pathname);
def cgroup_init_templates_cache(pathname: Union[c_char_p, bytes]) -> Union[c_int, int]: ...


# int cgroup_reload_cached_templates(char *pathname);
def cgroup_reload_cached_templates(pathname: Union[c_char_p, bytes]) -> Union[c_int, int]: ...


# int cgroup_config_create_template_group(struct cgroup *cgroup, char *template_name, int flags);
def cgroup_config_create_template_group(cgroup: CGroupPointer,
                                        template_name: Union[c_char_p, bytes],
                                        flags: DeleteFlag) -> Union[c_int, int]: ...
