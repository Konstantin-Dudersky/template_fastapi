#!/usr/bin/env python3
"""Установка poetry."""

import os
from typing import Callable


def main() -> Callable[[], None]:
    """Entry point."""

    def _main() -> None:
        os.system("sudo apt update")
        os.system("sudo apt install -y python3-venv curl")
        os.system("curl -sSL https://install.python-poetry.org | python3 -")
        print("""-> Если следующая команда выполняется с ошибкой
-> Command 'poetry' not found
-> нужно добавить в файл .bashrc
-> export PATH="$HOME/.local/bin:$PATH"
""")
        os.system(". ~/.profile && poetry config virtualenvs.in-project true")


    return _main


if __name__ == "__main__":
    main()
