#!/usr/bin/env python3
import asyncio
import functools
from contextlib import contextmanager
from time import time

import aiohttp
import requests
from os.path import basename
from datetime import datetime


# variables
IMG_DIR = 'images/'
URL = 'https://loremflickr.com/320/240'


# decorators --------------------------------------------------------------------------
def timer(foo):
    """function-decorator for sync functions"""

    def wrapper(*args, **kwargs):
        print(f'Start {foo.__name__}')
        start = datetime.now()
        result = foo(*args, **kwargs)
        print(f'{foo.__name__} is finished - execution time: {datetime.now() - start}')
        return result

    return wrapper


def a_timer(foo):
    """function-decorator for async functions"""

    @contextmanager
    def wrapping_logic():
        print(f'Start {foo.__name__}')
        start = datetime.now()
        yield
        print(f'{foo.__name__} is finished - execution time: {datetime.now() - start}')

    @functools.wraps(foo)
    def wrapper(*args, **kwargs):
        if not asyncio.iscoroutinefunction(foo):
            with wrapping_logic():
                return foo(*args, **kwargs)
        else:
            async def tmp():
                with wrapping_logic():
                    return await foo(*args, **kwargs)

            return tmp()

    return wrapper


# functions----------------------------------------------------------------------------
# synchronous functions
def get_file(url):
    response = requests.get(url, allow_redirects=True)
    return response


def write_file(response):
    filename = basename(response.url)
    with open(IMG_DIR + filename, 'wb') as f:
        f.write(response.content)


@timer
def main_s():
    for i in range(10):
        write_file(get_file(url=URL))


# asynchronous functions
def write_image(data):
    filename = f'{int(time()*1000)}.jpeg'
    with open(IMG_DIR + filename, 'wb') as f:
        f.write(data)


async def fetch_content(url, session):
    async with session.get(url) as response:
        data = await response.read()
        write_image(data)


@a_timer
async def main_a():
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i in range(10):
            tasks.append(asyncio.create_task(fetch_content(URL, session)))

        await asyncio.gather(*tasks)


if __name__ == '__main__':
    main_s()
    asyncio.run(main_a())
