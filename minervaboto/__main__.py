#!/usr/bin/env python3

from .minervaboto import renew_books, renewed_to_string
from .utils import *
import os
import pkg_resources
import sys

def do_renewal(user_id, user_pass, url):
    renewed = renew_books(user_id, user_pass, url)
    print(renewed_to_string(renewed))
    return renewed

def print_usage(executable, exit_code=None):
    print('Uso:')
    print('\t' + executable + '                   \tLê dados de login nas ' +
          'variáveis de ambiente.')
    print('\t' + executable + ' <id> <senha>      \tLê dados de login por ' +
          'parâmetros.')
    print('\t' + executable + ' --config [arquivo]\tLê dados de login em ' +
          'arquivo de configuração.')
    if exit_code: sys.exit(exit_code)

def main():
    executable = os.path.basename(sys.argv[0])
    url = 'https://minerva.ufrj.br/F'

    if len(sys.argv) == 3 and len(sys.argv[1]) > 0 and sys.argv[1][0] != '-':
        user_id = sys.argv[1]
        user_pass = sys.argv[2]
        do_renewal(user_id, user_pass, url)
    elif len(sys.argv) in [2, 3] and sys.argv[1] == '--config':
        if len(sys.argv) == 2:
            config_file = get_default_config_file('minervaboto', 'boto.conf')
        else:
            config_file = sys.argv[2]

        config = read_config_file(config_file)
        if not os.path.exists(config_file):
            if not config_first_run(config, config_file): sys.exit(0)

        user_id, user_pass = get_info_from_config(config)

        while True:
            if not (user_id and user_pass):
                print('Arquivo de configurações incompleto')
                user_id, user_pass = input_login_info(config, config_file)
                continue

            renewal = do_renewal(user_id, user_pass, url)

            if renewal['response']['code'] == 401:
                user_id, user_pass = input_login_info(config, config_file)
            else:
                break
    elif len(sys.argv) == 2 and sys.argv[1] == '--help':
        print_usage(executable, 0)
    elif len(sys.argv) == 2 and sys.argv[1] == '--version':
        print(pkg_resources.get_distribution('minervaboto').version)
        sys.exit(0)
    elif len(sys.argv) == 1:
        user_id, user_pass = get_env_vars(['MINERVA_ID', 'MINERVA_PASS'])
        if not (user_id and user_pass):
            print('Por favor, defina as variáveis \'MINERVA_ID\' e \'MINERVA_PASS\'.\n' +
                  'Execute `%s --help` para obter ajuda.' % executable, file=sys.stderr)
            sys.exit(1)
        do_renewal(user_id, user_pass, url)
    else:
        print_usage(executable, 1)

if __name__ == '__main__':
    main()
