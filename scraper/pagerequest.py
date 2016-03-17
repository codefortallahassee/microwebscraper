import requests


def get_page(url, **kwargs):
    response = requests.get(url, **kwargs)
    response.raise_for_status()
    return response.content
