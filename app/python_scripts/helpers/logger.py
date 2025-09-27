import logging
import sys

class logs:
    def __init__(self, filename: str = ""):
        self.filename = filename

        # Получаем root logger (главный)
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)

        # Проверяем, есть ли уже handler (чтобы не дублировать)
        if not root_logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                "%(asctime)s -  %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            root_logger.addHandler(handler)

        # ✅ Настраиваем логгеры Flask и Werkzeug
        for name in ("flask", "werkzeug"):
            flask_logger = logging.getLogger(name)
            flask_logger.setLevel(logging.INFO)
            flask_logger.propagate = True  # передаём в root

        # создаём логгер для текущего файла
        self.logger = logging.getLogger(__name__)

    def log_info(self, message: str):
        self.logger.info(f"{self.filename} - {message}")

    def log_error(self, message: str):
        self.logger.error(f"{self.filename} - {message}")