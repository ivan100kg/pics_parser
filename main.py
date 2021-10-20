#!/usr/bin/env python3
from os.path import basename

import requests
from bs4 import BeautifulSoup
import os


def get_response(url):
    """get response"""
    request = requests.get(url, headers={
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'})
    if request.status_code < 400:
        return request


def main():
    """main function"""
    url = 'https://ivash-ka.ru'

    if not os.path.exists('images/'):
        os.mkdir('images/')

    request = get_response(url + '/catalog/zhenskoe/')
    soup = BeautifulSoup(request.text, 'lxml')

    catalog_list = soup.find('div', {'class': 'catalog_list'})
    tag_links = catalog_list.find_all('a', {'class': 'name'})
    links = []
    for link in tag_links:
        links.append((link.text.strip(), url + link.get('href')))

    for link in links:
        dir_name = link[0]
        if not os.path.exists('images/' + dir_name):
            os.mkdir('images/' + dir_name)
        request = get_response(link[1])
        soup = BeautifulSoup(request.text, 'lxml')
        catalog_list = soup.find('div', {'class': 'catalog_list'})
        tag_pics = catalog_list.find_all('img')
        for pic in tag_pics:
            src = url + pic.get('data-original')
            with open(f'images/{dir_name}/{basename(src)}', 'wb') as f:
                f.write(requests.get(src).content)


if __name__ == '__main__':
    main()
