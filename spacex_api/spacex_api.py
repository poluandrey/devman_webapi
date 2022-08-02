import urllib.parse
from pathlib import Path
from typing import List

import requests

from utils.download_image import download_image
from utils.get_file_name_from_url import get_file_name_from_url


def get_list_of_spacex_images(url: str) -> List[str]:
    resp = requests.get(url)
    resp.raise_for_status()

    resp_json = resp.json()
    try:
        pictures = resp_json['links']['flickr']['original']
    except KeyError:
        raise Exception('internal error')
    return pictures


def fetch_spacex_last_launch(url: str, directory: Path, **kwargs) -> None:
    if 'latest' in kwargs:
        url = urllib.parse.urljoin(url, 'latest')
    if 'id' in kwargs:
        url = urllib.parse.urljoin(url, kwargs['id'])
    print(url)
    pictures_urls = get_list_of_spacex_images(url)
    print(pictures_urls)
    if len(pictures_urls) == 0:
        print('no image for download')
        return
    for url in pictures_urls:
        download_image(url, directory, file_name=get_file_name_from_url(url))
