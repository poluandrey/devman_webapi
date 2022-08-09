import posixpath
import urllib.parse
from collections import namedtuple
from datetime import date
from pathlib import Path
from typing import List, NamedTuple

import requests

from utils.utils import download_image, get_file_name_from_url

EpicDescr = namedtuple('EpicDescr', ['identifier', 'image'])


def get_apod_url(url: str, api_key, **kwargs) -> List[str]:
    url = urllib.parse.urljoin(url, '/planetary/apod')
    params = {'api_key': api_key}
    if 'img_count' in kwargs:
        params['count'] = kwargs['img_count']

    resp = requests.get(url, params=params)
    resp.raise_for_status()

    resp_json = resp.json()
    if isinstance(resp_json, List):
        image_urls = [img['url'] for img in resp_json]
        return image_urls
    return [resp_json['url']]


def retrieve_epic_images(url: str, token: str) -> List[NamedTuple]:
    params = {'api_key': token}
    url = urllib.parse.urljoin(url, 'EPIC/api/natural')
    resp = requests.get(url, params=params)
    resp.raise_for_status()

    images = []
    for img in resp.json():
        launch_date = img['identifier']
        img_date = date.fromisoformat(
            f'{launch_date[:4]}-{launch_date[4:6]}-{launch_date[6:8]}')
        descr = EpicDescr(img_date, img['image'])
        images.append(descr)

    return images


def download_epic_image(url: str,
                        token,
                        img_descr: List[EpicDescr], path) -> None:
    url = urllib.parse.urljoin(url, '/EPIC/archive/natural/')
    for img in img_descr:
        # extruct /y/m/d from file name
        url_part = posixpath.join(img.identifier.strftime('%Y'),
                                  img.identifier.strftime('%m'),
                                  img.identifier.strftime('%d'),
                                  'png',
                                  f'{img.image}.png')
        img_url = urllib.parse.urljoin(url, url_part)

        download_image(
            img_url,
            path,
            file_name=f'{img.image}.png',
            nasa_token=token)


def download_apod_image(urls: List[str], token: str, path: Path) -> None:
    for url in urls:
        download_image(
            url,
            path,
            file_name=get_file_name_from_url(url),
            nasa_token=token
        )
