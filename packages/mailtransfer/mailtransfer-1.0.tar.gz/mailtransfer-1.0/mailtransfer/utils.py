import os
import sys
import stat
from colorama import Fore, Style
from pathlib import Path


def get_config_path():
    home_dir = str(Path.home())
    config_file = ".mailtransfer/mailtransfer.cfg"
    config_file_path = os.path.join(home_dir, config_file)
    if os.path.exists(config_file_path):
        return config_file_path
    else:
        print("{}Config file ~/{} not found{}"
              .format(Fore.RED, config_file, Style.RESET_ALL))
        sys.exit(1)


def check_config_permissions(config_path):
    config_permissions = oct(stat.S_IMODE(os.lstat(config_path).st_mode))
    if config_permissions == "0o600":
        return True
    else:
        print("{}Config file {} have unsafely permissions (must be 0600).{}"
              .format(Fore.RED, config_path, Style.RESET_ALL))
        sys.exit(1)
