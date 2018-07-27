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

def get_return_dict(code, message=None, result=None):
    if not message: message = requests.status_codes._codes[code][0]
    return {'response': {'code': code, 'message': message}, 'result': result}

def get_link_from_js_replace_page(link):
    if link.startswith('http'):
        return link
    if not link.startswith('javascript:replacePage('):
        return None

    rst = link.replace('javascript:replacePage(\'', '')
    rst = rst.replace('\');', '')

    return rst

def parse_table(soup, books=[]):
    table = find_tag_containing_text(soup, 'table', 'Devolver em')
    if not table: return get_return_dict(422, 'Unable to find table')
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
    if response.status_code != 200: return get_return_dict(response.status_code)

    soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), default_parser)
    login_link = find_tag_containing_text(soup, 'a', 'Login')

    if not login_link: return get_return_dict(422, 'Unable to find login link')

    # NOTE(erick): Searching for the login form.
    response = requests.get(login_link.get('href'))
    if response.status_code != 200: return get_return_dict(response.status_code)

    soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), default_parser)
    form = soup.find('form')
    if not form.get('name') == 'form1':
        return get_return_dict(422, 'Unable to find form')

    action = form.get('action')
    func = get_input_named(form, 'func')
    bor_library = get_input_named(form, 'bor_library')

    if not (action and func and bor_library): return get_return_dict(422)

    payload = {
        'func' : func,
        'bor_id' : user_id,
        'bor_verification' : user_password,
        'bor_library' : bor_library,
        'x' : '0',
        'y' : '0'
    }

    response = requests.post(action, data=payload)
    if response.status_code != 200: return get_return_dict(response.status_code)

    # NOTE(ian): Checking if the login was successful.
    soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), default_parser)
    if find_tag_containing_text(soup, 'a', 'Login'):
        message = soup.find_all('td', class_='feedbackbar')[0]
        return get_return_dict(401, message.getText().strip())

    # NOTE(erick): Going to the borrowed books page.
    params = urlencode({'func': 'bor-loan', 'adm_library' : bor_library})
    url = action + "?" + params

    response = requests.get(url)
    if response.status_code != 200: return get_return_dict(response.status_code)

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
        return get_return_dict(response.status_code,
            'Você não tem livros para renovar', None)

    url = get_link_from_js_replace_page(renew_link.get('href'))
    if not url: return get_return_dict(422, 'No JS replacePage')
    response = requests.get(url)
    if response.status_code != 200: return get_return_dict(response.status_code)

    # NOTE(ian): Parsing the information table in the results page.
    soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), default_parser)
    books = parse_table(soup, books)

    return get_return_dict(200, None, books)

def books_to_string(books):
    total_renewed = 0
    next_renewal = None

    result = ''
    for idx, book in enumerate(books):
        if book['renewed_for']:
            total_renewed += 1
            renewed_for = ' (+%i dia%s)' % (book['renewed_for'].days,
                's' if book['renewed_for'].days > 1 else '')
        if not next_renewal or book['return_until'] < next_renewal:
            next_renewal = book['return_until']
        result += ('%i.\t%s' % (idx + 1, book['name'])) + '\n'
        result += ('\tDevolução: %s%s' %
            (datetime.strftime(book['return_until'], '%d/%m/%Y'),
             renewed_for if book['renewed_for'] else '')
        ) + '\n'
        result += '\tBiblioteca: ' + book['library'] + '\n'
        if book['issues']:
            result += '\tObservações: ' + book['issues'] + '\n'
        result += '\n'

    result += ('%s livro%s renovado%s. Data mais próxima para devolução: %s.' %
        (str(total_renewed) if total_renewed > 0 else 'Nenhum',
         's' if total_renewed > 1 else '', 's' if total_renewed > 1 else '',
         datetime.strftime(book['return_until'], '%d/%m/%Y'))
    )

    return result

def renewed_to_string(renewed):
    if renewed['result']:
        return books_to_string(renewed['result'])
    else:
        return (renewed['response']['message'])
