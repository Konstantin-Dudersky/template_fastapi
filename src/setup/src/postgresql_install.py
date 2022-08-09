#!/usr/bin/env python3
"""Установка PostgreSQL."""

import os
from typing import Callable


def main(system_version: str = "ubuntu-22.04") -> Callable[[], None]:
    """Entry point."""

    def _main() -> None:
        if system_version == "ubuntu-22.04":
            os.system("sudo apt install postgresql-14 libpq-dev")
            print("-> Установить пароль пользователя postgres:")
            print("-> ALTER USER postgres PASSWORD 'postgres';")
            print("-> после этого ввести:")
            print("-> exit")
            os.system("sudo -u postgres psql")
            print("-> для доступа к БД по сети в файле postgresql.conf:")
            print('-> listen_addresses = " * "')
            print("-> в файле pg_hba.conf:")
            print(
                """
host    all             all              0.0.0.0/0                       md5
host    all             all              ::/0                            md5
"""
            )

    return _main


if __name__ == "__main__":
    main()
