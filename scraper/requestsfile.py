from copy import deepcopy


def extract_request_args(xpaths_file):
    """Loads JSON xpaths file into requests dictionary

    :raises: KeyError
    """
    cfg = deepcopy(xpaths_file)
    url = cfg.pop('_url', None)
    return url, {k: v for k, v in cfg.items() if k.startswith('_')}
