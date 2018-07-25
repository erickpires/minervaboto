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

def parse_table(soup, books=[]):
    table = find_tag_containing_text(soup, 'table', 'Devolver em')
    assert table
    header = [th.getText().strip() for th in table.find_all('th')]
    pos = 0
    for rows in table.find_all('tr'):
        cells = [row.getText() for row in rows.find_all('td')]
        if len(cells) == 0: continue
        book = {} if len(books) == pos else books[pos]
        book['name'] = cells[header.index('Título' if 'Título' in header else 'Descrição')]
        if book['name'][-1] in ['.', ';', '/']:
            book['name'] = book['name'][:-1].strip()
        if 'Status do item' in header:
            book['status'] = cells[header.index('Status do item')]
        if 'Autor' in header:
            book['author'] = cells[header.index('Autor')]
        return_time = cells[header.index('Devolver em')]
        if 'Hora' in header:
            return_time += '  ' + cells[header.index('Hora')]
        return_time = datetime.strptime(return_time, '%d/%m/%y  %H:%M')
        if 'return_until' in book and return_time > book['return_until']:
            book['renewed_for'] = return_time - book['return_until']
        else:
            book['renewed_for'] = None
        book['return_until'] = return_time
        book['library'] = cells[header.index('Biblioteca')]
        if 'Número de renovações' in header:
            book['renewal_count'] = int(cells[header.index('Número de renovações')].split()[0])
        if 'Observação' in header:
            book['issues'] = cells[header.index('Observação')]
        elif  'Motivo para não renovação' in header:
            book['issues'] = cells[header.index('Motivo para não renovação')]

        if len(books) == pos: books.append(book)
        pos += 1
    return books

def renew_books(user_id, user_password, url='https://minerva.ufrj.br/F'):
    # NOTE(erick): Loading the front-page and looking for the login link
    response = requests.get(url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), default_parser)
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

    soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), default_parser)
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

    # NOTE(ian): Parsing the information table in the borrowed books page.
    soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), default_parser)
    books = parse_table(soup)

    # NOTE(erick): Searching for the 'Renovar Todos' link and renewing.
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

    # NOTE(ian): Parsing the information table in the results page.
    soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), default_parser)
    books = parse_table(soup, books)

    return books

def print_books(books):
    if len(books) == 0:
        print("Você não tem livros para renovar")
        return

    total_renewed = 0
    next_renewal = None

    for idx, book in enumerate(books):
        if book['renewed_for']:
            total_renewed += 1
            renewed_for = ' (+%i dia%s)' % (book['renewed_for'].days,
                's' if book['renewed_for'].days > 1 else '')
        if not next_renewal or book['return_until'] < next_renewal:
            next_renewal = book['return_until']
        print('%i.\t%s' % (idx + 1, book['name']))
        print('\tDevolução: %s%s' %
            (datetime.strftime(book['return_until'], '%d/%m/%Y'),
             renewed_for if book['renewed_for'] else '')
        )
        print('\tBiblioteca: ' + book['library'])
        if book['issues']:
            print('\tObservações: ' + book['issues'])
        print('')

    print('%s livro%s renovado%s. Data mais próxima para devolução: %s.' %
        (str(total_renewed) if total_renewed > 0 else 'Nenhum',
         's' if total_renewed > 1 else '', 's' if total_renewed > 1 else '',
         datetime.strftime(book['return_until'], '%d/%m/%Y'))
    )

def main():
    # NOTE(erick): Getting user id and password
    if not ('MINERVA_ID' in os.environ and
            'MINERVA_PASS' in os.environ):
        print('Please, set your \'MINERVA_ID\' and \'MINERVA_PASS\' environment variables.', file=sys.stderr)
        sys.exit(1)

    user_id = os.environ['MINERVA_ID']
    user_password = os.environ['MINERVA_PASS']
    url = 'https://minerva.ufrj.br/F'

    renewed = renew_books(user_id, user_password, url)

    print_books(renewed)


if __name__ == '__main__':
    main()
