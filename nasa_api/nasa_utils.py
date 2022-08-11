import posixpath
import urllib.parse
from collections import namedtuple
from datetime import date
from typing import List, NamedTuple, Any
from utils.utils import get_file_name_from_url

import requests

EpicDescr = namedtuple('EpicDescr', 'filename, image_url')


def get_apod_urls(url: str, api_key, img_count=None) -> List[str]:
    url = urllib.parse.urljoin(url, '/planetary/apod')
    params = {'api_key': api_key, 'count': img_count}

    resp = requests.get(url, params=params)
    resp.raise_for_status()

    apod_images = resp.json()
    if isinstance(apod_images, List):
        image_urls = [img['url'] for img in apod_images]
        return image_urls
    return [apod_images['url']]


def get_epic_info(epic_images: Any, url: str) -> List[NamedTuple]:
    url = urllib.parse.urljoin(url, '/EPIC/archive/natural/')
    images = []
    for img_url in epic_images:
        launch_date = img_url['identifier']
        img_date = date.fromisoformat(
            f'{launch_date[:4]}-{launch_date[4:6]}-{launch_date[6:8]}')
        url_part = posixpath.join(img_date.strftime('%Y'),
                                  img_date.strftime('%m'),
                                  img_date.strftime('%d'),
                                  'png',
                                  f'{img_url["image"]}.png')
        img_url = urllib.parse.urljoin(url, url_part)
        epic_descr = EpicDescr(get_file_name_from_url(img_url), img_url)
        images.append(epic_descr)

    return images
