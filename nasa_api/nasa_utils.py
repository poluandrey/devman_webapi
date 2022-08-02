from datetime import date
import posixpath
import urllib.parse
from collections import namedtuple
from typing import List, NamedTuple

import requests

from utils.download_image import download_image


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
        list_of_url = [img['url'] for img in resp_json]
        return list_of_url
    return [resp_json['url']]


def get_list_of_epic_img(url: str, token: str) -> List[NamedTuple]:
    params = {'api_key': token}
    url = urllib.parse.urljoin(url, 'EPIC/api/natural')
    resp = requests.get(url, params=params)
    resp.raise_for_status()

    imgs = []
    for img in resp.json():
        launch_date = img['identifier']
        img_date = date.fromisoformat(
            f'{launch_date[:4]}-{launch_date[4:6]}-{launch_date[6:8]}')
        descr = EpicDescr(img_date, img['image'])
        imgs.append(descr)

    return imgs


def download_epic_img(url: str,
                      token,
                      img_descr: List[EpicDescr], path) -> None:
    url = urllib.parse.urljoin(url, '/EPIC/archive/natural/')
    for img in img_descr:
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
