from urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth


class FITELnetAPIError(Exception):
    """FITELnet API errors."""

    pass


def request_api(func):
    """APIリクエストの共通処理を行うデコレーター。

    Args:
        func (Callable): APIリクエスト関数
    Returns:
        Callable: デコレーター適用後の関数
    """

    def wrapper(*args, **kwargs) -> requests.Response:
        res = func(*args, **kwargs)
        if res.status_code // 100 != 2:
            raise FITELnetAPIError(res.json().get("error"))

        return res

    return wrapper


def auth(
    bearer: bool, user: str | None, password: str | None, token: str | None
) -> dict:
    """認証データを作成する。
    Args:
        bearer (bool): Bearer認証を使用する場合はTrue、BASIC認証の場合はFalse
        user (str | None): BASIC認証時のユーザー名
        password (str | None): BASIC認証時のパスワード
        token (str | None): Bearer認証時のアクセストークン
    Returns:
        dict: requests用認証データ
    """
    if bearer:
        if token is None:
            raise ValueError("token must be set when using BEARER auth")
        headers = {"Authorization": f"Bearer {token}"}
        return {"headers": headers}
    else:
        if user is None or password is None:
            raise ValueError("user and password must be set when using BASIC auth")
        auth = HTTPBasicAuth(user, password)
        return {"auth": auth}


@request_api
def get(base_url: str, endpoint: str, auth: dict) -> requests.Response:
    """GETリクエストを送信する。

    Args:
        base_url (str): ベースURL
        endpoint (str): APIエンドポイントURL
        auth (dict): 認証情報
    Returns:
        requests.Response: レスポンスオブジェクト
    """

    return requests.get(url=urljoin(base_url, endpoint), **auth)


@request_api
def post(base_url: str, endpoint: str, auth: dict, data: dict) -> requests.Response:
    """POSTリクエストを送信する。

    Args:
        base_url (str): ベースURL
        endpoint (str): APIエンドポイントURL
        auth (dict): 認証情報
        data (dict): 送信するデータ
    Returns:
        requests.Response: レスポンスオブジェクト
    """

    return requests.post(url=urljoin(base_url, endpoint), json=data, **auth)
