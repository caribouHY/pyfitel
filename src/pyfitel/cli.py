from urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth

from .core import FITELnetAPIError, auth, get, post


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


def exec_commands(
    url: str,
    cmd_list: list[dict],
    user: str | None = None,
    password: str | None = None,
    bearer: bool = False,
    token: str | None = None,
) -> dict:
    """複数のCLI運用コマンドを実行する。

    Args:
        url (str): API URL
        cmd_list (list[dict]): 実行するコマンドのリスト
        user (str | None, optional): BASIC認証時のユーザー名
        password (str | None, optional): BASIC認証時のパスワード
        bearer (bool): Bearer認証を使用する場合はTrue、BASIC認証の場合はFalse
        token (str | None): Bearer認証時のアクセストークン
    Returns:
        dict:
    """
    if len(cmd_list) > 10:
        raise ValueError("A maximum of 10 commands can be executed at once.")
    if len(cmd_list) == 0:
        raise ValueError("At least one command must be provided.")

    api = "/api/v1/clis"
    data = {"list": cmd_list, "total": len(cmd_list)}

    res = post(
        base_url=url,
        endpoint=api,
        auth=auth(bearer=bearer, user=user, password=password, token=token),
        data=data,
    )
    return res.json()


def get_commands_result(
    url: str,
    cli_id: str,
    user: str | None = None,
    password: str | None = None,
    bearer: bool = False,
    token: str | None = None,
) -> dict:
    """指定したCLIコマンドIDの複数CLIコマンドの実行結果を取得する。

    Args:
        url (str): API URL
        cli_id (str): 取得するCLIコマンドID
        user (str | None, optional): BASIC認証時のユーザー名
        password (str | None, optional): BASIC認証時のパスワード
        bearer (bool): Bearer認証を使用する場合はTrue、BASIC認証の場合はFalse
        token (str | None): Bearer認証時のアクセストークン
    Returns:
        dict:
    """
    api = f"/api/v1/clis/{cli_id}"

    res = get(
        base_url=url,
        endpoint=api,
        auth=auth(bearer=bearer, user=user, password=password, token=token),
    )
    return res.json()
