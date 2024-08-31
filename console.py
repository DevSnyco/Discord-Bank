import traceback

from datetime import datetime

BOLD = "\033[1m"
LIGHTGRAY = "\033[37m"
GREY = "\033[90m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RED = "\033[31m"
RESET = "\033[0m"

class Console:
    @staticmethod
    def info(text: str):
        print(f"{GREY}{BOLD}{datetime.now().date()} {datetime.now().time().replace(microsecond=0)} {BLUE}{BOLD}INFO {RESET}{text}")

    @staticmethod
    def warn(text: str):
        print(f"{GREY}{BOLD}{datetime.now().date()} {datetime.now().time().replace(microsecond=0)} {YELLOW}{BOLD}WARNING{RESET} {LIGHTGRAY}{text}{RESET}")

    @staticmethod
    def error(exception: Exception):
        print(f"{GREY}{BOLD}{datetime.now().date()} {datetime.now().time().replace(microsecond=0)} {RED}{BOLD}ERROR{RESET}{RED}")
        traceback.print_exc(exception)