#!/usr/bin/env python3

from appdirs import user_config_dir
from os import path
import minervaboto
import configparser
import os
import sys

def write_config_file(config, config_file_path):
    with open(config_file_path, 'w') as f:
        config.write(f)

def input_login_info(config, config_file_path, operation):
    config["LOGIN"]["MINERVA_ID"] = input('ID/CPF: ')
    config["LOGIN"]["MINERVA_PASS"] = input('Senha (plain-text): ')

    write_config_file(config, config_file_path)

    print('Arquivo %s. Continuando...\n' % operation)

def main():
    boto_cfg_path = user_config_dir('minervaboto')
    config_file_path = path.join(boto_cfg_path, 'boto.conf')

    if not path.exists(boto_cfg_path):
        os.makedirs(boto_cfg_path)

    config = configparser.ConfigParser(default_section="LOGIN")
    config.read(config_file_path)

    if not path.exists(config_file_path):
        ans = input('Não encontramos um arquivo de configurações. Deseja ' +
                    'inserir os dados para login aqui? [s/N] ')
        if not ans.lower().strip() in ['s', 'sim']:
            print('Tudo bem. Por favor, insira seu ID e senha em: \n\t[%s]' %
                  config_file_path)
            config["LOGIN"]["MINERVA_ID"] = ''
            config["LOGIN"]["MINERVA_PASS"] = ''
            write_config_file(config, config_file_path)
            sys.exit(0)

        input_login_info(config, config_file_path, 'salvo')

    while True:
        try:
            user_id = config["LOGIN"]["MINERVA_ID"]
            user_password = config["LOGIN"]["MINERVA_PASS"]
            if not user_id or not user_password: raise(KeyError)
        except KeyError:
            print('Arquivo de configurações incompleto')
            input_login_info(config, config_file_path, 'atualizado')
            continue

        url = 'https://minerva.ufrj.br/F'
        renewed = minervaboto.renew_books(user_id, user_password, url)

        if renewed['result']:
            minervaboto.print_books(renewed['result'])
        else:
            print(renewed['response']['message'])

        if renewed['response']['code'] == 401:
            input_login_info(config, config_file_path, 'atualizado')
        else:
            break

if __name__ == '__main__':
    main()
