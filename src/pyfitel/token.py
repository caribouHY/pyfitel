from urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth

from .core import FITELnetAPIError


def publish_token(url: str, user: str, password: str) -> dict:
    """アクセストークンを発行する。

    Args:
        url (str): API URL
        user (str): ユーザー名
        password (str): パスワード
    Returns:
        dict: 発行されたアクセストークン情報
    """

    api = "/api/v1/token"
    api_url = urljoin(url, api)

    auth = HTTPBasicAuth(user, password)
    res = requests.post(url=api_url, auth=auth)

    if res.status_code // 100 != 2:
        raise FITELnetAPIError(res.json().get("error"))

    return res.json()


def delete_token(url: str, token: str) -> None:
    """アクセストークンを削除する。

    Args:
        url (str): API URL
        token (str): アクセストークン
    """

    api = "/api/v1/token"
    api_url = urljoin(url, api)
    api_url = f"{api_url}/{token}"

    headers = {"Authorization": f"Bearer {token}"}
    res = requests.delete(url=api_url, headers=headers)

    if res.status_code // 100 != 2:
        raise FITELnetAPIError(res.json().get("error"))
