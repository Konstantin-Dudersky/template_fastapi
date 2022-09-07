"""Работа с файлом настроек .env."""

import logging
from typing import Callable

from .cmd_in_dir import main

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def create(
    work_dir: str = "../server",
    command: str = "poetry run poe create_env",
) -> Callable[[], None]:
    """Создать файл с настройками.

    :param work_dir: относительный путь к папке
    :param command: команда
    :return: задача
    """

    def _task() -> None:
        log.info("Создаем файл с настройками")
        main(work_dir=work_dir, command=command)
        while True:
            log.warning(
                "Задайте настройки перед продолжением, после введите (y)",
            )
            ans: str = input()
            if ans == "y":
                break

    return _task
