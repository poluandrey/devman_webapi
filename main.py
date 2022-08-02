import argparse
import os.path
import sys
from pathlib import Path

import dotenv

from spacex_api.spacex_api import fetch_spacex_last_launch
from nasa_api.nasa_utils import get_list_of_epic_img, download_epic_img


def crete_dir(path):
    dir_name = 'images'
    full_path = path.joinpath(dir_name)
    Path(full_path).mkdir(parents=True, exist_ok=True)
    return full_path


def parse_args():
    parser = argparse.ArgumentParser(description='script for download images from via spacex or NASA API')
    parser.add_argument('--source', required=True, choices=('spacex', 'nasa'), help='choose image source')
    parser.add_argument('--launch_id', help='launch id')
    args = parser.parse_args()
    return args


def main():
    nasa_token = os.getenv('NASA_WEB_TOKEN')
    base_dir = Path(__file__).resolve().parent.parent
    img_dir = crete_dir(base_dir)
    args = parse_args()

    if args.source == 'nasa':
        nasa_base_url = 'https://api.nasa.gov'
        imgs = get_list_of_epic_img(nasa_base_url, nasa_token)
        download_epic_img(url=nasa_base_url, img_descr=imgs, path=img_dir, token=nasa_token, )
    else:
        spacex_url = 'https://api.spacexdata.com/v5/launches/'
        try:
            launch_id = args.launch_id
        except AttributeError:
            fetch_spacex_last_launch(spacex_url, directory=img_dir, latest=True)
            sys.exit()
        print(launch_id)
        fetch_spacex_last_launch(spacex_url, directory=img_dir, id=launch_id)


if __name__ == '__main__':
    dotenv.load_dotenv()
    main()
