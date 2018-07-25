#!/usr/bin/env python3

from appdirs import user_config_dir
from os import path
import minervaboto
import configparser
import os
import sys


def main():
    boto_cfg_path = user_config_dir('minervaboto')
    config_file_path = path.join(boto_cfg_path, 'boto.conf')

    if not path.exists(boto_cfg_path):
        os.makedirs(boto_cfg_path)

    config = configparser.ConfigParser(default_section="LOGIN")
    config.read(config_file_path)

    if not path.exists(config_file_path):
        ans = input('You don\'t have a config file. Do you want to enter' +
                    ' your credentials here? [y/N] ')
        if not ans.lower() in ['y', 'yes']:
            print('Ok. Please enter your id and password in: \n\t[%s]' %
                  config_file_path)
            config["LOGIN"]["MINERVA_ID"] = ''
            config["LOGIN"]["MINERVA_PASS"] = ''
            with open(config_file_path, 'w') as f:
                config.write(f)
            sys.exit(0)

        config["LOGIN"]["MINERVA_ID"] = input('Enter your id: ')
        config["LOGIN"]["MINERVA_PASS"] = input('Enter your password (plain-text): ')

        with open(config_file_path, 'w') as f:
            config.write(f)

        print('File saved. Continuing...\n')

    try:
        user_id = config["LOGIN"]["MINERVA_ID"]
        user_password = config["LOGIN"]["MINERVA_PASS"]
        if not user_id or not user_password: raise(KeyError)
    except KeyError:
        print('Config file is incomplete. Please verify it in: \n\t[%s]' %
              config_file_path)
        sys.exit(1)

    url = 'https://minerva.ufrj.br/F'
    renewed = minervaboto.renew_books(user_id, user_password, url)

    minervaboto.print_books(renewed)

if __name__ == '__main__':
    main()
