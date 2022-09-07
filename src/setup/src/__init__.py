"""Скрипты установки."""

from . import env
from . import https_certificate
from . import ng
from . import pgadmin
from . import poetry
from . import postgresql
from . import python
from . import simple_command
from .cmd_in_dir import main as cmd_in_dir
from .create_folder_abs import main as create_folder_abs
from .create_folder_rel import main as create_folder_rel
from .git_sync import main as git_sync
from .main import ComposeTask, Task, execute
from .port_redirect import main as port_redirect
from .postgresql_add_db import main as postgresql_add_db
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
    "env",
    "execute",
    "git_sync",
    "https_certificate",
    "ng",
    "pgadmin",
    "poetry",
    "port_redirect",
    "postgresql_add_db",
    "postgresql",
    "python",
    "samba",
    "simple_command",
    "systemd",
    "tauri_build",
    "timescaledb_install",
    "timescaledb_update_db",
]
