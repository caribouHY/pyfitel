from .core import auth, delete, get, post


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
        user (str | None): BASIC認証時のユーザー名
        password (str | None): BASIC認証時のパスワード
        bearer (bool): Bearer認証を使用する場合はTrue
        token (str | None): Bearer認証時のアクセストークン
    Returns:
        str: コマンド実行結果
    """

    api = "/api/v1/cli"
    data = {"cmd": cmd}

    res = post(
        base_url=url,
        endpoint=api,
        auth=auth(bearer=bearer, user=user, password=password, token=token),
        data=data,
    )
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
        user (str | None): BASIC認証時のユーザー名
        password (str | None): BASIC認証時のパスワード
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


def get_clis_id_all(
    url: str,
    user: str | None = None,
    password: str | None = None,
    bearer: bool = False,
    token: str | None = None,
) -> dict:
    """全てのCLIコマンドの複数実行のCLIコマンドIDを取得する。

    Args:
        url (str): API URL
        user (str | None): BASIC認証時のユーザー名
        password (str | None): BASIC認証時のパスワード
        bearer (bool): Bearer認証を使用する場合はTrue、BASIC認証の場合はFalse
        token (str | None): Bearer認証時のアクセストークン
    Returns:
        dict:
    """

    api = "/api/v1/clis"

    res = get(
        base_url=url,
        endpoint=api,
        auth=auth(bearer=bearer, user=user, password=password, token=token),
    )
    return res.json()


def delete_commands_result_all(
    url: str,
    user: str | None = None,
    password: str | None = None,
    bearer: bool = False,
    token: str | None = None,
) -> None:
    """全てのCLIコマンドの複数実行の結果を削除する。

    Args:
        url (str): API URL
        user (str | None): BASIC認証時のユーザー名
        password (str | None): BASIC認証時のパスワード
        bearer (bool): Bearer認証を使用する場合はTrue、BASIC認証の場合はFalse
        token (str | None): Bearer認証時のアクセストークン
    """

    api = "/api/v1/clis"
    delete(
        base_url=url,
        endpoint=api,
        auth=auth(bearer=bearer, user=user, password=password, token=token),
    )


def get_commands_result(
    url: str,
    clis_id: str,
    user: str | None = None,
    password: str | None = None,
    bearer: bool = False,
    token: str | None = None,
) -> dict:
    """指定したCLIコマンドIDの複数CLIコマンドの実行結果を取得する。

    Args:
        url (str): API URL
        cli_id (str): 取得するCLIコマンドID
        user (str | None): BASIC認証時のユーザー名
        password (str | None): BASIC認証時のパスワード
        bearer (bool): Bearer認証を使用する場合はTrue、BASIC認証の場合はFalse
        token (str | None): Bearer認証時のアクセストークン
    Returns:
        dict:
    """
    api = f"/api/v1/clis/{clis_id}"

    res = get(
        base_url=url,
        endpoint=api,
        auth=auth(bearer=bearer, user=user, password=password, token=token),
    )
    return res.json()


def delete_commands_result(
    url: str,
    clis_id: str,
    user: str | None = None,
    password: str | None = None,
    bearer: bool = False,
    token: str | None = None,
) -> None:
    """指定したCLIコマンドIDの複数CLIコマンドの実行結果を削除する。

    Args:
        url (str): API URL
        cli_id (str): 削除するCLIコマンドID
        user (str | None): BASIC認証時のユーザー名
        password (str | None): BASIC認証時のパスワード
        bearer (bool): Bearer認証を使用する場合はTrue、BASIC認証の場合はFalse
        token (str | None): Bearer認証時のアクセストークン
    """

    api = f"/api/v1/clis/{clis_id}"
    delete(
        base_url=url,
        endpoint=api,
        auth=auth(bearer=bearer, user=user, password=password, token=token),
    )
