#!/usr/bin/python3

from configobj import ConfigObj
from pathlib import Path
from .mailtransfer import MailTransfer
from .utils import get_config_path, check_config_permissions


def main():
    config_file_path = get_config_path()
    if check_config_permissions(config_file_path):
        config = ConfigObj(config_file_path)
        imap_server = config['imap_server']
        smtp_server = config['smtp_server']
        user_password = config['user_password']
        address_from = config['address_from']
        address_to = config['address_to']
        check_interval = config['check_interval']
        log_file = config['log_file']
        mt = MailTransfer(imap_server,
                          smtp_server,
                          address_from,
                          address_to,
                          user_password,
                          check_interval,
                          log_file)
        mt.run()


if __name__ == "__main__":
    main()
