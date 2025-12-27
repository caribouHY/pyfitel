from urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth

from .core import FITELnetAPIError


def exec_command(
    url: str,
    cmd: str,
    user: str | None = None,
    password: str | None = None,
    bearer: bool = False,
    token: str | None = None,
) -> str:
    """CLIの運用コマンドを実行する。

    Args:
        url (str): API URL
        cmd (str): 実行するコマンド
        user (str | None, optional): BASIC認証時のユーザー名
        password (str | None, optional): BASIC認証時のパスワード
        bearer (bool): Bearer認証を使用する場合はTrue
        token (str | None): Bearer認証時のアクセストークン
    Returns:
        str: コマンド実行結果
    """

    api = "/api/v1/cli"
    api_url = urljoin(url, api)
    data = {"cmd": cmd}

    if bearer:
        if token is None:
            raise ValueError("token must be set when using BEARER auth")
        res = requests.post(
            url=api_url, json=data, headers={"Authorization": f"Bearer {token}"}
        )
    else:
        if user is None or password is None:
            raise ValueError("user and password must be set when using BASIC auth")
        auth = HTTPBasicAuth(user, password)
        res = requests.post(url=api_url, json=data, auth=auth)

    if res.status_code // 100 != 2:
        raise FITELnetAPIError(res.json().get("error"))
    return res.text
