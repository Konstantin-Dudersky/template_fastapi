#!/usr/bin/env python3
"""Скрипты установки."""

import sys
from typing import NamedTuple

import src

POETRY_VERSION: str = "1.2.0"
PYTHON_VERSION: str = "3.10.6"

SYSTEMD_SERVICE_API = "coca_api"

DB_CONF: str = "db_conf"
DB_DATA: str = "db_data"


class Tasks(NamedTuple):
    apt_update_upgrade: src.Task = src.Task(
        desc="Обновление системы",
        task=src.simple_command.execute(
            command="sudo apt update && sudo apt upgrade",
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
    https_certificate: src.Task = src.Task(
        desc="Создать сертификат https",
        task=src.https_certificate.create("coca"),
    )
    pgadmin_install: src.Task = src.Task(
        desc="Установка pgAdmin",
        task=src.pgadmin.install(),
    )
    poetry_self_install: src.Task = src.Task(
        desc="Установить в системе poetry",
        task=src.poetry.self_install(POETRY_VERSION),
    )
    poetry_check_version: src.Task = src.Task(
        desc="Проверка версии poetry",
        task=src.poetry.check_version(),
    )
    port_redirect_443_8000: src.Task = src.Task(
        desc="Перенаправление портов",
        task=src.port_redirect(from_port=443, to_port=8000),
    )
    postgresql_install: src.Task = src.Task(
        desc="Установить БД postgresql",
        task=src.postgresql.install("ubuntu-22.04"),
    )
    psycopg2_depends: src.Task = src.Task(
        desc="Зависимости для psycopg2",
        task=src.simple_command.execute(
            command="sudo apt install python3-dev",
        ),
    )
    python_install: src.Task = src.Task(
        desc="Установка python",
        task=src.python(PYTHON_VERSION),
    )
    server_alembic_check: src.Task = src.Task(
        desc="Проверить актуальность схемы БД",
        task=src.cmd_in_dir(
            work_dir="../server",
            command="poetry run alembic-autogen-check",
        ),
    )
    server_create_env: src.Task = src.Task(
        desc="Создать файл .env с настройками",
        task=src.cmd_in_dir(
            work_dir="../server",
            command="poetry run poe create_env",
        ),
    )
    server_db_conf_create: src.Task = src.Task(
        desc=f"Создать БД для конфигурации {DB_CONF}",
        task=src.postgresql_add_db(DB_CONF),
    )

    server_db_conf_scheme: src.Task = src.Task(
        desc="Обновить схему БД db_conf",
        task=src.cmd_in_dir(
            work_dir="../server",
            command="poetry run alembic upgrade head",
        ),
    )
    server_db_data_create: src.Task = src.Task(
        desc=f"Создать БД для данных {DB_DATA}",
        task=src.postgresql_add_db(DB_DATA),
    )
    server_db_data_install_timescale: src.Task = src.Task(
        desc="Установка TimescaleDB",
        task=src.timescaledb_update_db(DB_DATA),
    )
    server_db_data_scheme: src.Task = src.Task(
        desc=f"Создать схему БД {DB_DATA}",
        task=src.cmd_in_dir(
            work_dir="../server",
            command="poetry run poe db_data_scheme",
        ),
    )
    server_lint: src.Task = src.Task(
        desc="linting",
        task=src.cmd_in_dir(
            work_dir="../server",
            command="poetry run poe lint",
        ),
    )
    server_systemd_api_create: src.Task = src.Task(
        desc="Создание сервиса systemd",
        task=src.systemd(
            service_name=SYSTEMD_SERVICE_API,
            description="SYSTEMD_SERVICE_API",
            work_dir_relative="../server",
        ),
    )
    server_systemd_api_start: src.Task = src.Task(
        desc="Запустить сервис API",
        task=src.cmd_in_dir(
            work_dir=".",
            command=f"sudo systemctl start {SYSTEMD_SERVICE_API}",
        ),
    )
    server_systemd_api_stop: src.Task = src.Task(
        desc="Остановить сервис API",
        task=src.cmd_in_dir(
            work_dir=".",
            command=f"sudo systemctl stop {SYSTEMD_SERVICE_API}",
        ),
    )
    server_poetry_update: src.Task = src.Task(
        desc="Обновление пакетов poetry",
        task=src.cmd_in_dir(
            work_dir="../server",
            command="poetry update --only main",
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
    webapp_build: src.Task = src.Task(
        desc="Сборка проекта Angular в webapp",
        task=src.ng_build(
            work_dir_relative="../webapp",
            project="webapp",
            base_href="/app/",
        ),
    )
    webapp_dist: src.Task = src.Task(
        desc="Распаковать файлы webapp",
        task=src.ng_dist(
            source_dir_rel="../webapp",
            target_dir_rel="../server/static",
            project="webapp",
        ),
    )
    webapp_docs: src.Task = src.Task(
        desc="Документация webapp",
        task=src.cmd_in_dir(
            work_dir="../webapp",
            command=(
                "npx compodoc -p tsconfig.doc.json "
                "--output ../../docs/webapp"
            ),
        ),
    )
    webapp_format: src.Task = src.Task(
        desc="Форматирование исходников webapp",
        task=src.cmd_in_dir(
            work_dir="../webapp",
            command="npx prettier --write src",
        ),
    )


TASKS: Tasks = Tasks()


class ComposeTasks(NamedTuple):
    build: src.ComposeTask = src.ComposeTask(
        desc="Сборка проекта",
        subtasks=[
            TASKS.server_lint,
            TASKS.server_alembic_check,
            TASKS.webapp_format,
            TASKS.webapp_build,
            TASKS.webapp_docs,
        ],
    )
    install_server_1: src.ComposeTask = src.ComposeTask(
        desc="Установка проекта сервере, ч. 1",
        subtasks=[
            TASKS.apt_update_upgrade,
            TASKS.poetry_self_install,
            TASKS.port_redirect_443_8000,
            TASKS.https_certificate,
            TASKS.psycopg2_depends,
            # db prepare
            TASKS.postgresql_install,
            TASKS.timescaledb_install,
            TASKS.pgadmin_install,
        ],
    )
    install_server_2: src.ComposeTask = src.ComposeTask(
        desc="Установка проекта на сервере, ч. 2",
        subtasks=[
            TASKS.poetry_check_version,
            TASKS.server_poetry_update,
            TASKS.server_create_env,
            # db setup
            TASKS.server_db_conf_create,
            TASKS.server_db_conf_scheme,
            TASKS.server_db_data_create,
            TASKS.server_db_data_install_timescale,
            TASKS.server_db_data_scheme,
            # other
            TASKS.server_systemd_api_create,
            # TASKS.server_share_folder,
            # TASKS.webapp_dist,
        ],
    )
    install_iot: src.ComposeTask = src.ComposeTask(
        desc="Установка проекта на IOT",
        subtasks=[
            TASKS.python_install,
        ],
    )
    update_server: src.ComposeTask = src.ComposeTask(
        desc="Обновить проект на сервере",
        subtasks=[
            TASKS.server_systemd_api_stop,
            TASKS.apt_update_upgrade,
            TASKS.git_sync,
            TASKS.server_poetry_update,
            TASKS.server_create_env,
            TASKS.webapp_dist,
            TASKS.server_db_conf_scheme,
            TASKS.server_systemd_api_start,
        ],
    )
    update_iot: src.ComposeTask = src.ComposeTask(
        desc="Обновить проект на IOT",
        subtasks=[],
    )


COMPOSE_TASKS: ComposeTasks = ComposeTasks()


if __name__ == "__main__":
    src.execute(sys.argv, TASKS, COMPOSE_TASKS)
