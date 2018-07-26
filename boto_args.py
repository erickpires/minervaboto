#!/usr/bin/env python3

import minervaboto
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: {} user_id user_password" .format(sys.argv[0]))
        sys.exit(1)

    url = 'https://minerva.ufrj.br/F'
    renewed = minervaboto.renew_books(sys.argv[1], sys.argv[2], url)

    if renewed['result']:
        minervaboto.print_books(renewed['result'])
    else:
        print(renewed['response']['message'])
if __name__ == '__main__':
    main()
