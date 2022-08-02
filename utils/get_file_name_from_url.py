import os
import urllib.parse


def get_file_name_from_url(url: str) -> str:
    url_parse = urllib.parse.urlsplit(url)
    path = urllib.parse.unquote(url_parse.path)
    _, file_name = os.path.split(path)
    return file_name
