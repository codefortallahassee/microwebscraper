import requests
from copy import deepcopy


def request_page(url, **kwargs):
    response = requests.get(url, **kwargs)
    response.raise_for_status()
    return response.content


def get_request_settings(config):
    """Pull requests.get settings from config dictionary"""
    cfg = deepcopy(config)
    url = cfg.pop('_url', None)
    return url, {k: v for k, v in cfg.items() if k.startswith('_')}


def load_html_page(config, page=None, url=None):
    if page:
        return page.read()

    requests_url, requests_kwargs = get_request_settings(config)
    return request_page(url if url else requests_url, **requests_kwargs)
