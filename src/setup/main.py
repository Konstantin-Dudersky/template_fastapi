#!/usr/bin/env python3
"""Скрипты установки."""

import sys
from typing import NamedTuple

import src


SYSTEMD_SERVICE = "kleck"
POETRY_VERSION: str = "1.1.14"
PYTHON_VERSION: str = "3.10.6"


class Tasks(NamedTuple):
    # build --------------------------------------------------------------------
    webapp_format: src.Task = src.Task(
        desc="Форматирование исходников webapp",
        task=src.cmd_in_dir(
            work_dir="../client",
            command="npx prettier --write src",
        ),
    )
    # --------------------------------------------------------------------------


    client_ng_build: src.Task = src.Task(
        desc="Сборка проекта Angular",
        task=src.ng_build(work_dir_relative="../client", project="client"),
    )
    client_ng_dist: src.Task = src.Task(
        desc="Распаковать файлы фронтенда",
        task=src.ng_dist(
            source_dir_rel="../client",
            target_dir_rel="../server/static",
            project="client",
        ),
    )
    client_tauri_build: src.Task = src.Task(
        desc="Сборка tauri",
        task=src.tauri_build(
            work_dir_relative="../client",
            project="client",
        ),
    )
    git_sync: src.Task = src.Task(
        desc="Синхронизировать проект через git",
        task=src.git_sync(),
    )
    pgadmin: src.Task = src.Task(
        desc="Установка pgAdmin",
        task=src.pgadmin(),
    )
    poetry_self_install: src.Task = src.Task(
        desc="Установить в системе poetry",
        task=src.poetry_self_install(POETRY_VERSION),
    )
    postgresql_add_db: src.Task = src.Task(
        desc="Создать базу данный в postgresql",
        task=src.postgresql_add_db("test_db"),
    )
    postgresql_install: src.Task = src.Task(
        desc="Установить БД postgresql",
        task=src.postgresql_install("ubuntu-22.04"),
    )
    python_install: src.Task = src.Task(
        desc="Установка python",
        task=src.python("3.10.5"),
    )
    server_alembic_upgrade: src.Task = src.Task(
        desc="Обновить схему БД",
        task=src.cmd_in_dir(
            work_dir="../server",
            command=". ~/.profile && poetry run alembic upgrade head",
        ),
    )
    server_lint: src.Task = src.Task(
        desc="linting",
        task=src.cmd_in_dir(
            work_dir="../server",
            command="poetry run poe lint",
        ),
    )
    server_service_start: src.Task = src.Task(
        desc="Запустить сервис",
        task=src.cmd_in_dir(
            work_dir=".",
            command=f"sudo systemctl start {SYSTEMD_SERVICE}",
        ),
    )
    server_service_stop: src.Task = src.Task(
        desc="Остановить сервис",
        task=src.cmd_in_dir(
            work_dir=".",
            command=f"sudo systemctl stop {SYSTEMD_SERVICE}",
        ),
    )
    server_poetry_update: src.Task = src.Task(
        desc="Обновление пакетов poetry",
        task=src.cmd_in_dir(
            work_dir="../server",
            command=". ~/.profile && poetry update --no-dev",
        ),
    )
    server_port_redirect: src.Task = src.Task(
        desc="Перенаправление портов",
        task=src.port_redirect(from_port=80, to_port=8000),
    )
    server_systemd: src.Task = src.Task(
        desc="Создание сервиса systemd",
        task=src.systemd(
            service_name=SYSTEMD_SERVICE,
            description="kleck",
            work_dir_relative="../server",
        ),
    )
    server_share_folder: src.Task = src.Task(
        desc="Создание общей папки",
        task=src.samba("../../share"),
    )
    timescaledb_install: src.Task = src.Task(
        desc="Установка TimescaleDB",
        task=src.timescaledb_install("ubuntu-22.04"),
    )
    timescaledb_update_db: src.Task = src.Task(
        desc="Установка TimescaleDB",
        task=src.timescaledb_update_db("test_db"),
    )
    webapp_docs: src.Task = src.Task(
        desc="Документация webapp",
        task=src.cmd_in_dir(
            work_dir="../client",
            command="npm run compodoc",
        ),
    )


TASKS = Tasks()


class ComposeTasks(NamedTuple):
    build: src.ComposeTask = src.ComposeTask(
        desc="Сборка проекта",
        subtasks=[
            TASKS.server_lint,
            TASKS.client_ng_build,
            TASKS.webapp_format,
            TASKS.webapp_docs,
        ],
    )
    install: src.ComposeTask = src.ComposeTask(
        desc="Установка проекта на целевой системе",
        subtasks=[
            TASKS.python_install,
            TASKS.poetry_self_install,
            TASKS.server_port_redirect,
            TASKS.server_systemd,
            TASKS.server_share_folder,
        ],
    )
    update: src.ComposeTask = src.ComposeTask(
        desc="Обновить проект на целевой системе",
        subtasks=[
            TASKS.server_service_stop,
            TASKS.git_sync,
            TASKS.server_poetry_update,
            TASKS.client_ng_dist,
            TASKS.server_alembic_upgrade,
            TASKS.server_service_start,
        ],
    )


COMPOSE_TASKS = ComposeTasks()


if __name__ == "__main__":
    src.execute(sys.argv, TASKS, COMPOSE_TASKS)
