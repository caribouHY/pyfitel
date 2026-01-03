from .core import auth, delete, post


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

    res = post(
        base_url=url,
        endpoint=api,
        auth=auth(bearer=False, user=user, password=password, token=None),
        data=None,
    )

    return res.json()


def delete_token(url: str, token: str) -> None:
    """アクセストークンを削除する。

    Args:
        url (str): API URL
        token (str): アクセストークン
    """

    api = f"/api/v1/token/{token}"

    delete(
        base_url=url,
        endpoint=api,
        auth=auth(bearer=True, user=None, password=None, token=token),
    )
