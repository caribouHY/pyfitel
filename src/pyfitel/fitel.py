import time

from .cli import delete_commands_result, exec_command, exec_commands, get_commands_result
from .config import update_config


class CLI:
    def __init__(self, cmd: str, on_fail_exit: bool = False) -> None:
        self._cmd = cmd
        self._on_fail_action = "exit" if on_fail_exit else "continue"

    def to_dict(self) -> dict:
        return {
            "cmd": self._cmd,
            "on_fail": {"action": self._on_fail_action},
        }


class FITELnetAPI:
    def __init__(self, host: str, port: int, user: str, password: str, tls: bool) -> None:
        """
        Args:
            host (str): 機器のIPアドレスまたはFQDN
            port (int): ポート番号
            user (str): ユーザー名
            password (str): パスワード
            tls (bool): httpsの場合はTrue,httpの場合はFalse
        """
        self._url = "http"
        if tls:
            self._url += "s"
        self._url = f"{self._url}://{host}:{port}/"

        self._user = user
        self._password = password
        self._bearer = False

    def _get_auth(self) -> dict:
        return {
            "url": self._url,
            "user": self._user,
            "password": self._password,
            "bearer": self._bearer,
            "token": None,
        }

    def command(self, cmd: str) -> str:
        """運用管理コマンドを実行する。

        Args:
            cmd (str): 実行するコマンド

        Returns:
            str: コマンド実行結果
        """
        return exec_command(cmd=cmd, **self._get_auth())

    def commands_wait(
        self,
        cmd_list: list[CLI] | list[str] | list[str | CLI],
        wait: float = 0.5,
        retries: int = 5,
        interval: float = 1.0,
        delete: bool = True,
    ) -> dict:
        """複数のCLI運用コマンドを実行し、完了まで待機する。

        Args:
            cmd_list (list[CLI] | list[str] | list[str | CLI]): CLIコマンドのリスト
            wait (float, optional): CLI実行後の初回待機秒数
            retries (int, optional): リトライ回数
            interval (float, optional): リトライ間隔(秒)
            delete (bool, optional): コマンド実行結果取得後に実行結果を機器から削除するかどうか

        Raises:
            ValueError: retries must be 0 or more
            TimeoutError: Command execution did not complete within the specified retries.

        Returns:
            dict: CLIコマンド実行結果
        """
        if retries < 0:
            raise ValueError("retries must be 0 or more")

        clis = {
            "list": [cmd.to_dict() if isinstance(cmd, CLI) else CLI(str(cmd)).to_dict() for cmd in cmd_list],
            "total": len(cmd_list),
        }
        res = exec_commands(cmd_list=clis["list"], **self._get_auth())
        clis_id = res["clis_id"]

        time.sleep(wait)
        for _ in range(retries + 1):
            res = get_commands_result(clis_id=clis_id, **self._get_auth())
            if res["status"] != "Processing":
                if delete:
                    delete_commands_result(clis_id=clis_id, **self._get_auth())
                return res
            time.sleep(interval)
        raise TimeoutError("Command execution did not complete within the specified retries.")

    def config(self, config: bytes | str | list[str], commit: bool = True) -> None:
        """構成定義を変更する

        Args:
            config (bytes | str | list[str]): 構成定義
            commit (bool, optional): 構成定義適用後にcommitを実行すうるかどうか. デフォルトはTrue
        """
        if isinstance(config, list):
            config = "\n".join(config).encode()
        update_config(config=config, **self._get_auth())
        if commit:
            self.command("commit")
