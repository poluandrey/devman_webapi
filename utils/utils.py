import os
import urllib.parse

import requests


def get_file_name_from_url(url: str) -> str:
    url_parse = urllib.parse.urlsplit(url)
    path = urllib.parse.unquote(url_parse.path)
    _, file_name = os.path.split(path)
    return file_name


def download_image(url: str, path, file_name='image.png', **kwargs) -> None:
    params = {}
    if 'nasa_token' in kwargs:
        params['api_key'] = kwargs['nasa_token']

    resp = requests.get(url, params=params)
    resp.raise_for_status()

    with open(path.joinpath(file_name), 'wb') as file_out:
        file_out.write(resp.content)
