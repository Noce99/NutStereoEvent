import os
import sys
from termcolor import colored


def green(string):
    return colored(string, "green", attrs=["bold"])


def red(string):
    return colored(string, "red", attrs=["bold"])


def yellow(string):
    return colored(string, "yellow", attrs=["bold"])


def check_python_version():
    detected_python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(green(f"Detected Python version: {detected_python_version}"))
    if sys.version_info.major != 3:
        print(red("You need python 3!"))
        exit()
    elif sys.version_info.minor != 12:
        print(yellow(f"The code was tested with python 3.12.3. (detected {detected_python_version})"
              f" Anyway let's try, finger cross..."))
    elif sys.version_info.micro != 3:
        print(yellow(f"The code was tested with python 3.12.3.  (detected {detected_python_version})"
              f" Anyway let's try, finger cross..."))


if __name__ == "__main__":
    pass