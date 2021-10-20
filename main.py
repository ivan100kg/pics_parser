#!/usr/bin/env python3
from os.path import basename

import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime


def timer(foo):
    """function-decorator"""
    def wrapper(*args, **kwargs):
        print(f'Start {foo.__name__}')
        start = datetime.now()
        result = foo(*args, **kwargs)
        print(f'{foo.__name__} is finished - execution time: {datetime.now() - start}')
        return result
    return wrapper


def get_response(url):
    """This function returns response from url"""
    request = requests.get(url, headers={
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'})
    if request.status_code < 400:
        return request
    else:
        return None


async def async_func():
    """asynchronous function"""
    pass


@timer
def sync_func():
    """synchronous function"""

    # set variables
    url = 'https://ivash-ka.ru'
    women_clothes = '/catalog/zhenskoe/'
    pic_dir = 'images/'
    request = get_response(url + women_clothes)
    soup = BeautifulSoup(request.text, 'lxml')

    # check dir
    if not os.path.exists(pic_dir):
        os.mkdir(pic_dir)

    # image search
    tag_links = soup.find_all('a', {'class': 'name'})
    data = []  # list of (category name, category url)
    [data.append((tag_link.text.strip(), url + tag_link.get('href'))) for tag_link in tag_links]
    # get name and url from data
    for category_name, category_url in data:
        dir_name = category_name
        # check dirs
        if not os.path.exists(pic_dir + dir_name):
            os.mkdir(pic_dir + dir_name)
        # getting responses from pages and search images
        request = get_response(category_url)
        soup = BeautifulSoup(request.text, 'lxml')
        # catalog_list = soup.find('div', {'class': 'catalog_list'})
        # tag_pics = catalog_list.find_all('img', {'class': 'lazy'})
        tag_pics = soup.find_all('img', {'class': 'lazy'})
        # save images to storage
        for pic in tag_pics:
            src = url + pic.get('data-original')
            with open(f'{pic_dir}{dir_name}/{basename(src)}', 'wb') as f:
                f.write(requests.get(src).content)


if __name__ == '__main__':
    sync_func()
