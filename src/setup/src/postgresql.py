"""Установка PostgreSQL.

user:password - postgres:postgres
"""

import logging
import os
from typing import Callable


def install(system_version: str = "ubuntu-22.04") -> Callable[[], None]:
    """Entry point.

    :param system_version: версия ОС
    :return: задача
    """

    def _main() -> None:
        if system_version == "ubuntu-22.04":
            logging.info("Установка PostgreSQL v14")
            os.system("sudo apt install postgresql-14 libpq-dev")
            os.system(
                """
echo "ALTER USER postgres PASSWORD 'postgres';" | sudo -u postgres psql
"""
            )
            logging.warning("Для доступа к БД по сети заменить файлы:")
            logging.warning("\n/etc/postgresql/14/main/postgresql.conf:")
            logging.warning('\nlisten_addresses = " * "')
            logging.warning("\n/etc/postgresql/14/main/pg_hba.conf:")
            logging.warning(
                """
host    all             all              0.0.0.0/0                       md5
host    all             all              ::/0                            md5
""",
            )
            logging.warning("\nПосле изменения перезагрузить сервис:\n")
            logging.warning("sudo systemctl restart postgresql.service")
            logging.warning("sudo systemctl restart postgresql.service")
            logging.warning("\nПользователь и пароль по-умолчанию:")
            while True:
                logging.info("-> Продолжить ? (y)")
                ans = input()
                if ans == "y":
                    break

    return _main


if __name__ == "__main__":
    install()
