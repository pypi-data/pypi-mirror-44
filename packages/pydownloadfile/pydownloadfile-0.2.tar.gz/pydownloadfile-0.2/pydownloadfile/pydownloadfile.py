#!/usr/bin/env python3

from requests import get
from typing import Any, Dict, Optional

from os.path import basename

type_none_or_dict = Optional[Dict[Any, Any]]


def download_file(
    url: str,
    file_name: Optional[str] = None,
    headers: type_none_or_dict = None,
    proxies: type_none_or_dict = None
        ) -> None:
    """
    Download a file using requests.

    :param url: str:
        Url of the file to be downloaded.
    :param file_name: str:
        File name to be written. (Default value = None)
    :param headers: type_none_or_dict:
        Requests's headers. (Default value = None)
    :param proxies: type_none_or_dict:
        Requests's proxies (Default value = None)

    """
    # If file_name is not provided it will be derived from url.
    if not file_name:
        file_name = basename(url)

    with open(file_name, "wb") as f:
        f.write(
            get(
                url,
                headers=headers,
                proxies=proxies
                ).content
            )
