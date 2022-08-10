import posixpath
import urllib.parse
from collections import namedtuple
from datetime import date
from typing import List, NamedTuple, Any

import requests

EpicDescr = namedtuple('EpicDescr', ['image', 'image_url'])


def get_apod_urls(url: str, api_key, img_count=None) -> List[str]:
    url = urllib.parse.urljoin(url, '/planetary/apod')
    params = {'api_key': api_key, 'count': img_count}

    resp = requests.get(url, params=params)
    resp.raise_for_status()

    data = resp.json()
    if isinstance(data, List):
        image_urls = [img['url'] for img in data]
        return image_urls
    return [data['url']]


def retrieve_epic_images(url: str, token: str) -> List[NamedTuple]:
    url = urllib.parse.urljoin(url, 'EPIC/api/natural')
    params = {'api_key': token}
    resp = requests.get(url, params=params)

    resp.raise_for_status()
    return resp.json()


def get_epic_image_info(data: Any, url: str) -> List[NamedTuple]:
    url = urllib.parse.urljoin(url, '/EPIC/archive/natural/')
    images = []
    for img in data:
        launch_date = img['identifier']
        img_date = date.fromisoformat(
            f'{launch_date[:4]}-{launch_date[4:6]}-{launch_date[6:8]}')
        url_part = posixpath.join(img_date.strftime('%Y'),
                                  img_date.strftime('%m'),
                                  img_date.strftime('%d'),
                                  'png',
                                  f'{img["image"]}.png')
        img_url = urllib.parse.urljoin(url, url_part)
        descr = EpicDescr(img['image'], img_url)
        images.append(descr)

    return images
