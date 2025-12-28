from .core import auth, patch, put


def replace_config(
    url: str,
    config: bytes | str,
    user: str | None = None,
    password: str | None = None,
    bearer: bool = False,
    token: str | None = None,
) -> str:
    """ルータの設定を置き換える。

    Args:
        url (str): API URL
        config (bytes | str):
        user (str | None): BASIC認証時のユーザー名
        password (str | None): BASIC認証時のパスワード
        bearer (bool): Bearer認証を使用する場合はTrue
        token (str | None): Bearer認証時のアクセストークン
    Returns:
        str: コンフィグ適用結果
    """

    api = "/api/v1/config"

    if not isinstance(config, bytes):
        config = str(config).encode()

    res = put(
        base_url=url, endpoint=api, auth=auth(bearer=bearer, user=user, password=password, token=token), data=config
    )
    return res.text


def update_config(
    url: str,
    config: bytes | str,
    user: str | None = None,
    password: str | None = None,
    bearer: bool = False,
    token: str | None = None,
) -> str:
    """ルータの設定の差分反映(追加・削除・変更)を行う。

    Args:
        url (str): API URL
        config (bytes | str):
        user (str | None): BASIC認証時のユーザー名
        password (str | None): BASIC認証時のパスワード
        bearer (bool): Bearer認証を使用する場合はTrue
        token (str | None): Bearer認証時のアクセストークン
    Returns:
        str: コンフィグ適用結果
    """
    api = "/api/v1/config"

    if not isinstance(config, bytes):
        config = str(config).encode()

    res = patch(
        base_url=url, endpoint=api, auth=auth(bearer=bearer, user=user, password=password, token=token), data=config
    )
    return res.text
