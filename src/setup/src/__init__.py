"""Скрипты установки."""

from .cmd_in_dir import main as cmd_in_dir
from .create_folder_abs import main as create_folder_abs
from .create_folder_rel import main as create_folder_rel
from .git_sync import main as git_sync
from .main import ComposeTask, Task, execute
from .ng_build import main as ng_build
from .ng_dist import main as ng_dist
from .pgadmin import main as pgadmin
from .poetry import poetry_self_install, poetry_self_update
from .port_redirect import main as port_redirect
from .postgresql_add_db import main as postgresql_add_db
from .postgresql_install import main as postgresql_install
from .python import main as python
from .samba import main as samba
from .systemd import main as systemd
from .tauri_build import main as tauri_build
from .timescaledb_install import main as timescaledb_install
from .timescaledb_update_db import main as timescaledb_update_db

__all__ = [
    "ComposeTask",
    "Task",
    "cmd_in_dir",
    "create_folder_abs",
    "create_folder_rel",
    "execute",
    "git_sync",
    "ng_build",
    "ng_dist",
    "pgadmin",
    "poetry_self_install",
    "poetry_self_update",
    "port_redirect",
    "postgresql_add_db",
    "postgresql_install",
    "python",
    "samba",
    "systemd",
    "tauri_build",
    "timescaledb_install",
    "timescaledb_update_db",
]
