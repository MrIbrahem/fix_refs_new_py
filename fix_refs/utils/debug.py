"""
Debug and testing utilities
"""

DEBUG: bool = False
TEST_MODE: bool = False


def echo_test(msg: str) -> None:
    """Print message if in test mode"""
    if TEST_MODE:
        print(msg)


def echo_debug(msg: str) -> None:
    """Print message if DEBUG is True"""
    if DEBUG:
        print(msg)
