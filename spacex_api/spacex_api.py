import urllib.parse
from pathlib import Path
from typing import List

import requests

from utils.utils import download_image, get_file_name_from_url


def retrieve_spacex_images_url(url: str) -> List[str]:
    """get list of images url from launch"""
    resp = requests.get(url)
    resp.raise_for_status()

    resp_json = resp.json()
    try:
        images = resp_json['links']['flickr']['original']
    except KeyError:
        raise Exception('internal error')
    return images


def fetch_spacex_launch(url: str, directory: Path, **kwargs) -> None:
    if 'id' in kwargs:
        url = urllib.parse.urljoin(url, kwargs['id'])
    else:
        url = urllib.parse.urljoin(url, 'latest')
    images_urls = retrieve_spacex_images_url(url)
    if len(images_urls) == 0:
        print('no image for download')
        return
    for url in images_urls:
        download_image(url, directory, file_name=get_file_name_from_url(url))
