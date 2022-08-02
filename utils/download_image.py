import requests


def download_image(url: str, path, **kwargs) -> None:
    params = {}
    if 'file_name' in kwargs:
        file_name = kwargs['file_name']
    else:
        file_name = 'image.png'
    if 'nasa_token' in kwargs:
        params['api_key'] = kwargs['nasa_token']

    resp = requests.get(url, params=params)
    resp.raise_for_status()

    with open(path.joinpath(file_name), 'wb') as file_out:
        file_out.write(resp.content)
