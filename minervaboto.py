#!/usr/bin/env python3

from bs4 import BeautifulSoup
from urllib.parse import urlencode
import requests
import sys
import os

default_parser = 'html.parser'

#
# Code
#

def get_input_named(form, name):
    for _input in form.find_all('input'):
        if _input.get('name') == name:
            return _input.get('value')

    return None


#
# Main
#

# NOTE(erick): Getting user id and password
if not ('MINERVA_ID' in os.environ and
        'MINERVA_PASS' in os.environ):
    print('Please, set your \'MINERVA_ID\' and \'MINERVA_PASS\' environment variables.', file=sys.stderr)
    sys.exit(1)

user_id = os.environ['MINERVA_ID']
user_password = os.environ['MINERVA_PASS']


# NOTE(erick): Loading the front-page and looking for the login link
url = 'https://minerva.ufrj.br/F'

response = requests.get(url)
soup = BeautifulSoup(response.text, default_parser)

login_link = None
for link in soup.find_all('a'):
    link_text = link.getText().strip()

    if link_text == 'Login':
        login_link = link
        break

if login_link == None:
    print('Unable to find login link', file=sys.stderr)
    sys.exit(1)

# NOTE(erick): Searching for the login form.
response = requests.get(login_link.get('href'))
soup = BeautifulSoup(response.text, default_parser)

form = soup.find('form')
assert form.get('name') == 'form1'

action = form.get('action')
func         = get_input_named(form, 'func')
bor_library  = get_input_named(form, 'bor_library')

# print("Action: " + action)
# print("func: "         + func)
# print("bor_library: "  + bor_library)

payload = {
    'func' : func,
    'bor_id' : user_id,
    'bor_verification' : user_password,
    'bor_library' : bor_library,
    'x' : '0',
    'y' : '0'
}

response = requests.post(action, data=payload)

# NOTE(erick): Going to the borrowed books page.
params = urlencode({'func': 'bor-loan', 'adm_library' : bor_library})
url = action + "?" + params

response = requests.get(url)

print(response.text)
