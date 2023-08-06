"""
where the helpers go
"""
import datetime
import errno
import os
import requests
from mimir_cli.globals import PACKAGE, __version__
from distutils.version import StrictVersion


def js_ts_to_str(_timestamp):
    """returns a nice date string from a js timestamp"""
    return datetime.datetime.fromtimestamp(_timestamp / 1000).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def mkdir(path):
    """creates a folder if it doesnt exist"""
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def get_versions():
    """fetch versions of mimir-cli"""
    response = requests.get("https://pypi.python.org/pypi/{}/json".format(PACKAGE))
    versions = list(response.json()["releases"].keys())
    versions.sort(key=StrictVersion, reverse=True)
    return versions


def is_latest():
    """check if we have the latest (or later) version of mimir-cli"""
    latest = StrictVersion(get_versions()[0])
    current = StrictVersion(__version__)
    return current >= latest
