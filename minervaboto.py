#!/usr/bin/env python3

from bs4 import BeautifulSoup
from urllib.parse import urlencode
from datetime import datetime
import requests
import sys
import os

default_parser = 'html.parser'

#
# Code
#

def get_input_named(form, name):
    result = form.find('input', {'name' : name})
    if result:
        return result.get('value')

    return None

def find_tag_containing_text(soup, tag, text):
    for item in soup.find_all(tag):
        if text in item.getText():
            return item

    return None

def get_link_from_js_replace_page(link):
    if link.startswith('http'):
        return link
    if not link.startswith('javascript:replacePage('):
        raise ValueError('Error: No JS replacePage')

    rst = link.replace('javascript:replacePage(\'', '')
    rst = rst.replace('\');', '')

    return rst

def renew_books(url, user_id, user_password):
    # NOTE(erick): Loading the front-page and looking for the login link
    response = requests.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.text, default_parser)
    login_link = None
    for link in soup.find_all('a'):
        link_text = link.getText().strip()

        if link_text == 'Login':
            login_link = link
            break

    if not login_link:
        raise ValueError('Unable to find login link')

    # NOTE(erick): Searching for the login form.
    response = requests.get(login_link.get('href'))
    assert response.status_code == 200

    soup = BeautifulSoup(response.text, default_parser)
    form = soup.find('form')
    assert form.get('name') == 'form1'

    action = form.get('action')
    func         = get_input_named(form, 'func')
    bor_library  = get_input_named(form, 'bor_library')

    assert action
    assert func
    assert bor_library

    payload = {
        'func' : func,
        'bor_id' : user_id,
        'bor_verification' : user_password,
        'bor_library' : bor_library,
        'x' : '0',
        'y' : '0'
    }

    response = requests.post(action, data=payload)
    assert response.status_code == 200

    # NOTE(erick): Going to the borrowed books page.
    params = urlencode({'func': 'bor-loan', 'adm_library' : bor_library})
    url = action + "?" + params

    response = requests.get(url)
    assert response.status_code == 200

    # NOTE(erick): Searching for the 'Renovar Todos' link and renewing.
    soup = BeautifulSoup(response.text, default_parser)

    renew_link = None
    for link in soup.find_all('a'):
        link_text = link.getText().strip()

        if link_text == 'Renovar Todos':
            renew_link = link
            break

    if not renew_link:
        return []

    url = get_link_from_js_replace_page(renew_link.get('href'))
    response = requests.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.text, default_parser)
    table = find_tag_containing_text(soup, 'table', 'Devolver em')
    assert table

    # NOTE(erick): Parsing the information table.
    books = []
    for rows in table.find_all('tr'):
        cells = rows.find_all('td')
        if len(cells) == 0:
            continue

        book = {}
        book['name'] = cells[1].getText()
        book['status'] = cells[2].getText()
        book['return_in'] = datetime.strptime(cells[3].getText(), '%d/%m/%y')
        book['library'] = cells[5].getText()
        book['issues'] = cells[8].getText()

        books.append(book)

    return books

def main():
    # NOTE(erick): Getting user id and password
    if not ('MINERVA_ID' in os.environ and
            'MINERVA_PASS' in os.environ):
        print('Please, set your \'MINERVA_ID\' and \'MINERVA_PASS\' environment variables.', file=sys.stderr)
        sys.exit(1)

    user_id = os.environ['MINERVA_ID']
    user_password = os.environ['MINERVA_PASS']
    url = 'https://minerva.ufrj.br/F'

    renewed = renew_books(url, user_id, user_password)

    if len(renewed) == 0:
        print("Você não tem livros para renovar")
        return

    for book in renewed:
        print('Nome: ' + book['name'])
        print('\Devolução: ' + datetime.strftime(book['return_in'], '%d/%m/%y'))
        print('\tBiblioteca: ' + book['library'])
        if book['issues']:
            print('\tObservações: ' + book['issues'])
        print('')


if __name__ == '__main__':
    main()
