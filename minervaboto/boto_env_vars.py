#!/usr/bin/env python3

import minervaboto
import os
import sys

def env_vars():
    # NOTE(erick): Getting user id and password
    if not ('MINERVA_ID' in os.environ and
            'MINERVA_PASS' in os.environ):
        print('Please, set your \'MINERVA_ID\' and \'MINERVA_PASS\' environment variables.', file=sys.stderr)
        sys.exit(1)

    user_id = os.environ['MINERVA_ID']
    user_password = os.environ['MINERVA_PASS']
    url = 'https://minerva.ufrj.br/F'

    renewed = minervaboto.renew_books(user_id, user_password, url)
    print(minervaboto.renewed_to_string(renewed))
