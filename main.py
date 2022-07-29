import datetime
import os.path
import posixpath
import urllib.parse
from collections import namedtuple
from pathlib import Path
from typing import List, NamedTuple

import dotenv
import requests

EpicDescr = namedtuple('EpicDescr', ['identifier', 'image'])


def crete_dir(path):
    dir_name = 'images'
    full_path = path.joinpath(dir_name)
    Path(full_path).mkdir(parents=True, exist_ok=True)
    return full_path


def get_list_of_spacex_images(url: str) -> List[str]:
    resp = requests.get(url)
    resp.raise_for_status()

    resp_json = resp.json()
    try:
        pictures = resp_json['links']['flickr']['original']
    except KeyError:
        raise Exception('internal error')
    return pictures


def fetch_spacex_last_launch(url: str, directory: Path) -> None:
    pictures_urls = get_list_of_spacex_images(url)

    for file_id, url in enumerate(pictures_urls):
        download_image(url, directory, file_name=f'spacex_{file_id}')


def download_image(url: str, path, **kwargs) -> None:
    print(kwargs)
    params = {}
    if 'file_name' in kwargs:
        file_name = kwargs['file_name']
    if 'nasa_token' in kwargs:
        params['api_key'] = kwargs['nasa_token']
    else:
        file_name = 'image.png'
    resp = requests.get(url, params=params)
    resp.raise_for_status()

    with open(path.joinpath(file_name), 'wb') as file_out:
        file_out.write(resp.content)


def get_file_name_from_url(url: str) -> str:
    url_parse = urllib.parse.urlsplit(url)
    path = urllib.parse.unquote(url_parse.path)
    _, file_name = os.path.split(path)
    # extension = os.path.splitext(file_name)[1]
    return file_name


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
        date = img['identifier']
        img_date = datetime.date.fromisoformat(f'{date[:4]}-{date[4:6]}-{date[6:8]}')
        descr = EpicDescr(img_date, img['image'])
        imgs.append(descr)

    return imgs


def download_epic_img(url: str, token, img_descr: List[EpicDescr], path) -> None:
    url = urllib.parse.urljoin(url, '/EPIC/archive/natural/')
    for img in img_descr:
        url_part = posixpath.join(img.identifier.strftime('%Y'),
                                  img.identifier.strftime('%m'),
                                  img.identifier.strftime('%d'),
                                  'png',
                                  f'{img.image}.png')
        img_url = urllib.parse.urljoin(url, url_part)

        download_image(img_url, path, file_name=f'{img.image}.png', nasa_token=token)


def main():
    nasa_token = os.getenv('NASA_WEB_TOKEN')
    base_dir = Path(__file__).resolve().parent.parent
    spacex_url = 'https://api.spacexdata.com/v5/launches/5eb87d47ffd86e000604b38a'
    picture_url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'
    nasa_base_url = 'https://api.nasa.gov'
    nasa_epic_url = 'https://api.nasa.gov/EPIC/api/natural'
    img_dir = crete_dir(base_dir)
    # download_image(picture_url, dir)
    # fetch_spacex_last_launch(spacex_url, dir)

    # apod_url = get_apod_url(url=nasa_base_url, api_key=nasa_token, img_count=5)
    # img_urls = apod_url
    # for url in img_urls:
    #     file_name = get_file_name_from_url(url)
    #     download_image(url, img_dir, file_name=file_name)

    imgs = get_list_of_epic_img(nasa_base_url, nasa_token)
    download_epic_img(url=nasa_base_url, img_descr=imgs, path=img_dir, token=nasa_token,)


if __name__ == '__main__':
    dotenv.load_dotenv()
    main()
