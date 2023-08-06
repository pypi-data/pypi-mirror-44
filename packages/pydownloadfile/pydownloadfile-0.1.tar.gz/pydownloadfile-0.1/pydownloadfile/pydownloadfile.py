#!/usr/bin/env python3

from requests import get
from typing import Any, Dict, Optional

type_none_or_dict = Optional[Dict[Any, Any]]


def download_file(
    url: str,
    file_name: str,
    headers: type_none_or_dict = None,
    proxies: type_none_or_dict = None
        ) -> None:
    """
    Download a file using requests.

    :param url: str: Url of the file to be downloaded.
    :param file_name: str: File name to be written.
    :param headers: type_none_or_dict:
        Requests's headers. (Default value = None)
    :param proxies: type_none_or_dict:
        Requests's proxies (Default value = None)

    """
    with open(file_name, "wb") as f:
        f.write(
            get(
                url,
                headers=headers,
                proxies=proxies
                ).content
            )
