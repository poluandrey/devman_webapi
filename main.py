import argparse
import os.path
import sys
from pathlib import Path

import dotenv

from nasa_api.nasa_utils import (download_epic_image, get_apod_url,
                                 retrieve_epic_images)
from spacex_api.spacex_api import fetch_spacex_launch
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
        help='choose type of image for download'
    )
    parser.add_argument(
        '--launch_id',
        help='spacex launch id, if blank download image from latest launch')
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
            imgs = retrieve_epic_images(nasa_base_url, nasa_token)
            download_epic_image(
                url=nasa_base_url,
                img_descr=imgs,
                path=img_dir,
                token=nasa_token
            )
        elif args.nasa_img_type == 'apod':
            imgs = get_apod_url(url=nasa_base_url, api_key=nasa_token)
            for url in imgs:
                download_image(
                    url,
                    img_dir,
                    file_name=get_file_name_from_url(url),
                    nasa_token=nasa_token
                )
        else:
            print('please specify --nasa_img_type')

    else:
        spacex_url = 'https://api.spacexdata.com/v5/launches/'
        launch_id = args.launch_id
        if launch_id is None:
            fetch_spacex_launch(
                spacex_url,
                directory=img_dir)
            sys.exit()
        fetch_spacex_launch(spacex_url, directory=img_dir, id=launch_id)


if __name__ == '__main__':
    main()
