#!/usr/bin/env python3

from appdirs import user_config_dir
from configparser import ConfigParser
from getpass import getpass
from os import path
import minervaboto
import os
import sys

def write_config_file(config, config_file_path):
    with open(config_file_path, 'w') as f:
        config.write(f)

def input_login_info(config, config_file_path, operation):
    user_id = config['LOGIN']['MINERVA_ID']
    config['LOGIN']['MINERVA_ID'] = str(
        input('ID/CPF%s: ' % (' [%s]' % user_id if user_id else '')) or user_id)
    config['LOGIN']['MINERVA_PASS'] = getpass('Senha: ')

    write_config_file(config, config_file_path)
    print('Arquivo %s. Continuando...\n' % operation)

def config_file():
    boto_cfg_path = user_config_dir('minervaboto')
    config_file_path = path.join(boto_cfg_path, 'boto.conf')

    if not path.exists(boto_cfg_path):
        os.makedirs(boto_cfg_path)

    config = ConfigParser(default_section='LOGIN')
    config.read(config_file_path)

    login = config['LOGIN']
    for required_key in ['MINERVA_ID', 'MINERVA_PASS']:
        if not required_key in login: login[required_key] = ''

    if not path.exists(config_file_path):
        ans = input('Não encontramos um arquivo de configurações. Deseja ' +
                    'inserir os dados para login aqui? [s/N] ')
        if not ans.lower().strip() in ['s', 'sim']:
            print('Tudo bem. Por favor, insira seu ID e senha em: \n\t[%s]' %
                  config_file_path)
            write_config_file(config, config_file_path)
            sys.exit(0)

        input_login_info(config, config_file_path, 'salvo')

    while True:
        if not (login['MINERVA_ID'] and login['MINERVA_PASS']):
            print('Arquivo de configurações incompleto')
            input_login_info(config, config_file_path, 'atualizado')
            continue

        url = 'https://minerva.ufrj.br/F'
        renewed = minervaboto.renew_books(login['MINERVA_ID'], login['MINERVA_PASS'], url)

        print(minervaboto.renewed_to_string(renewed))

        if renewed['response']['code'] == 401:
            input_login_info(config, config_file_path, 'atualizado')
        else:
            break
