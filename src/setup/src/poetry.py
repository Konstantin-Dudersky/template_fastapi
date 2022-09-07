"""Установка poetry."""

import logging
import os
from typing import Callable

from ._shared import get_logger

log = get_logger(__name__, logging.DEBUG)

POETRY_BIN: str = "~/.local/share/pypoetry/venv/bin/poetry"


def self_install(version: str = "1.2.0") -> Callable[[], None]:
    """Установить в системе poerty.

    :param version: версия для установки
    :return: функция
    """

    def _main() -> None:
        log.info("Версия poetry в системе:")
        os.system("poetry --version")
        while True:
            log.info("-> Установить ? (y/n)")
            ans = input()
            if ans == "y":
                break
            elif ans == "n":
                return
        os.system(
            "sudo apt install -y python3-venv curl python3-dev build-essential"
        )
        os.system(
            "curl -sSL https://install.python-poetry.org"
            f" | python3 - --version {version}",
        )
        os.system(f"{POETRY_BIN} config virtualenvs.in-project true")

    return _main


def self_update(version: str = "1.2.0") -> Callable[[], None]:
    """Обновить poetry.

    :param version: версия для обновления
    :return: задача
    """

    def _main() -> None:
        log.info("Версия poetry в системе:")
        os.system("poetry --version")
        while True:
            log.info("-> Обновить ? (y/n)")
            ans = input()
            if ans == "y":
                break
            elif ans == "n":
                return
        os.system(f"poetry self update {version}")

    return _main


def check_version() -> Callable[[], None]:
    """Проверка, что poetry установлена.

    :return: задача
    """

    def _main() -> None:
        log.info("Версия poetry в системе:")
        os.system("poetry --version")
        log.warning(
            "Если версия poetry не найдена, необходимо "
            "добавить в файл ~/.bashrc:",
        )
        log.warning('\nexport PATH="$HOME/.local/bin:$PATH"')
        log.warning(
            "\nПосле перезапустить систему и "
            "продолжить установку с этого шага",
        )

    return _main
