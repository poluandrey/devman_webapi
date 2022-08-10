import urllib.parse
from typing import List

import requests


def retrieve_spacex_images_url(url: str, launch_id=None) -> List[str]:
    """get list of images url from launch"""
    if launch_id is not None:
        url = urllib.parse.urljoin(url, launch_id)
    else:
        url = urllib.parse.urljoin(url, 'latest')
    resp = requests.get(url)
    resp.raise_for_status()

    data = resp.json()
    return data['links']['flickr']['original']
