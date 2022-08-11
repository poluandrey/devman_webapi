import argparse
import os.path
import urllib.parse
from pathlib import Path

import dotenv
import requests

from nasa_api.nasa_utils import get_apod_urls, get_epic_info
from utils.utils import download_image, get_file_name_from_url


def crete_dir(path):
    """create directory for image download"""
    dir_name = 'images'
    full_path = path.joinpath(dir_name)
    Path(full_path).mkdir(parents=True, exist_ok=True)
    return full_path


def parse_args():
    parser = argparse.ArgumentParser(
        description='script for download images via spacex or NASA API')
    parser.add_argument(
        '--source',
        required=True,
        choices=('spacex', 'nasa'),
        help='choose image source')
    parser.add_argument(
        '--nasa_img_type',
        choices=('apod', 'epic'),
        help='choose type of image for download',
        default='apod'
    )
    parser.add_argument(
        '--launch_id',
        help='spacex launch id, if blank download image from latest launch',
        default='latest'
    )
    args = parser.parse_args()
    return args


def main():
    dotenv.load_dotenv()
    nasa_token = os.getenv('NASA_WEB_TOKEN')
    base_dir = Path(__file__).resolve().parent.parent
    img_dir = crete_dir(base_dir)
    args = parse_args()

    if args.source == 'nasa':
        nasa_base_url = 'https://api.nasa.gov'
        if args.nasa_img_type == 'epic':
            url = urllib.parse.urljoin(nasa_base_url, 'EPIC/api/natural')
            params = {'api_key': nasa_token}
            resp = requests.get(url, params=params)

            resp.raise_for_status()

            json_content = resp.json()

            epics = get_epic_info(json_content, nasa_base_url)
            for epic in epics:
                download_image(
                    epic.image_url,
                    img_dir,
                    file_name=epic.filename,
                    nasa_token=nasa_token
                )
        elif args.nasa_img_type == 'apod':
            images = get_apod_urls(url=nasa_base_url, api_key=nasa_token)
            for url in images:
                download_image(
                    url,
                    img_dir,
                    file_name=get_file_name_from_url(url),
                    nasa_token=nasa_token
                )
    else:
        spacex_url = 'https://api.spacexdata.com/v5/launches/'
        launch_id = args.launch_id

        url = urllib.parse.urljoin(spacex_url, launch_id)
        resp = requests.get(url)
        resp.raise_for_status()

        data = resp.json()
        try:
            images = data['links']['flickr']['original']
        except KeyError:
            print('image not found')
            return
        if not images:
            print('no images for download')
            return
        for url in images:
            download_image(
                url,
                img_dir,
                file_name=get_file_name_from_url(url),
            )


if __name__ == '__main__':
    main()
