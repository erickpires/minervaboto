#!/usr/bin/env python3

from .boto_args import args
from .boto_config_file import config_file
from .boto_env_vars import env_vars

import sys
import os

def main():
    if len(sys.argv) == 3:
        args()
    elif len(sys.argv) == 2 and sys.argv[1] == '--config':
        config_file()
    elif len(sys.argv) == 2 and sys.argv[1] == '--version':
        print('1.0.4')
    elif len(sys.argv) == 1:
        env_vars()
    else:
        executable = os.path.basename(sys.argv[0])
        print('Usage:')
        print('\t' + executable + ' <id> <password>')
        print('\t' + executable + '           * reads credentials from'+
              ' environment variables.')
        print('\t' + executable + ' --config  * reads credentials from config file')

        sys.exit(1)

if __name__ == '__main__':
    main()
