#!/usr/bin/env python3

from appdirs import user_config_dir
from os import path
import minervaboto
import os
import sys


def main():
    boto_cfg_path = user_config_dir('minervaboto')
    config_file_path = path.join(boto_cfg_path, 'boto.conf')

    if not path.exists(boto_cfg_path):
        os.makedirs(boto_cfg_path)

    if not path.exists(config_file_path):
        ans = input('You don\'t have a config file. Do you want to enter' +
                    ' your credentials here? [y/N]')
        if not 'y' in ans:
            print('Ok. Please enter your id and password in: \n\t[{}]'.
                  format(config_file_path))
            sys.exit(0)

        m_id = input('Enter your id:')
        passwd = input('Enter your password (Plain-text): ')

        with open(config_file_path, 'w') as f:
            print('MINERVA_ID = {}'.format(m_id), file=f)
            print('MINERVA_PASS = {}'.format(passwd), file=f)

        print('Thanks')

    user_id = None
    user_password = None
    with open(config_file_path) as input_file:
        for line in input_file:
            if 'MINERVA_ID =' in line:
                user_id = line.replace('MINERVA_ID =', '').strip()
            if 'MINERVA_PASS =' in line:
                user_password = line.replace('MINERVA_PASS =', ''.strip())

    if not user_id or not user_password:
        print('Config file has invalid content. Please verify it.')
        sys.exit(1)


    url = 'https://minerva.ufrj.br/F'
    renewed = minervaboto.renew_books(user_id, user_password, url)

    minervaboto.print_books(renewed)

if __name__ == '__main__':
    main()
