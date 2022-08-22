import logging
from logging import Handler
from typing import List

FORMAT: str = "%(message)s"


# logging ----------------------------------------------------------------------


class StreamFormatter(logging.Formatter):
    """Custom formatter."""

    GREEN: str = "\x1b[32;20m"
    GREY: str = "\x1b[38;20m"
    YELLOW: str = "\x1b[33;20m"
    RED: str = "\x1b[31;20m"
    BOLD_RED: str = "\x1b[31;1m"
    RESET: str = "\x1b[0m"

    def get_format(self: "StreamFormatter", text: str, levelno: int) -> str:
        """Цвет сообщения.

        :param text: текст, цвет которого нужно изменить
        :param levelno: класс сообщения
        :return: текст с измененным текстом
        """
        if levelno == logging.DEBUG:
            return self.GREY + text + self.RESET
        if levelno == logging.INFO:
            return self.GREEN + text + self.RESET
        if levelno == logging.WARNING:
            return self.YELLOW + text + self.RESET
        if levelno == logging.ERROR:
            return self.RED + text + self.RESET
        if levelno == logging.CRITICAL:
            return self.BOLD_RED + text + self.RESET
        return text

    def format(self: "StreamFormatter", record: logging.LogRecord) -> str:
        """Format function.

        :param record: запись логгера
        :return: отформатированная запись логгера
        """
        log_fmt = self.get_format(FORMAT, record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


_handlers: List[Handler] = []
# логгирование в консоль
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(StreamFormatter())
_handlers.append(stream_handler)

logging.basicConfig(
    format=FORMAT,
    level=logging.INFO,
    handlers=_handlers,
)


def get_logger(
    name: str,
    level: int = logging.INFO,
) -> logging.Logger:
    """Return logger with name.

    :param name: название логгера
    :param level: уровень логгирования
    :return: объект логгера
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger
