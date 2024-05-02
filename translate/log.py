ANSI_RESET = "\033[0m"
ANSI_RED = "\033[31m"
ANSI_GREEN = "\033[32m"
ANSI_YELLOW = "\033[33m"
ANSI_BLUE = "\033[34m"

ERROR_TAG = f"[{ANSI_RED}E{ANSI_RESET}]"
INFO_TAG = f"[{ANSI_GREEN}I{ANSI_RESET}]"
WARN_TAG = f"[{ANSI_YELLOW}W{ANSI_RESET}]"
DEBUG_TAG = f"[{ANSI_BLUE}D{ANSI_RESET}]"


def tx_error(msg):
    print(f"{ERROR_TAG} {msg}")


def tx_info(msg):
    print(f"{INFO_TAG} {msg}")


def tx_warn(msg):
    print(f"{WARN_TAG} {msg}")


def tx_debug(msg):
    print(f"{DEBUG_TAG} {msg}")
