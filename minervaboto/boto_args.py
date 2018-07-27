#!/usr/bin/env python3

import minervaboto
import sys

def args():
    url = 'https://minerva.ufrj.br/F'
    renewed = minervaboto.renew_books(sys.argv[1], sys.argv[2], url)

    print(minervaboto.renewed_to_string(renewed))
