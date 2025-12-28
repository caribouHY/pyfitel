import json

import pytest
from pytest_mock import MockFixture

from pyfitel import exec_command, exec_commands, get_commands_result

from .common import MockReponse


def test_exec_command(mocker: MockFixture):
    command_result = """
--------------------- present-side ---------------------
F70   Version 01.16(01)[0]00.00.0 [2025/11/06 15:00]

---------------------- other-side ----------------------
F70   Version 01.08(00)b0[0]00.00.0 [2023/06/30 15:00]
"""
    mock_api = mocker.patch(
        "pyfitel.cli.post",
        return_value=MockReponse(status_code=201, text=command_result),
    )

    url = "http://192.168.1.1:55443"
    cmd = "show version"
    user = "operator"
    password = "password123"

    result = exec_command(url=url, cmd=cmd, user=user, password=password, bearer=False)

    assert mock_api.call_count == 1
    assert result == command_result


def test_get_commands_result(mocker: MockFixture):
    relust_data = {
        "clis_id": 1,
        "status": "success",
        "list": [
            {
                "cmd": "show version",
                "on_fail": {"action": "exit"},
                "result": "success",
                "message": "The result of the command execution is in Contents.",
                "contents": [
                    "",
                    "  --------------------- present-side --------------------- ",
                    "F70   Version 01.16(01)[0]00.00.0 [2025/11/06 15:00]",
                    "",
                    "  ---------------------- other-side ---------------------- ",
                    "F70   Version 01.08(00)b0[0]00.00.0 [2023/06/30 15:00]",
                    "",
                    "",
                ],
            },
            {
                "cmd": "show ip route | search grep 192",
                "on_fail": {"action": "continue"},
                "result": "success",
                "message": "The result of the command execution is in Contents.",
                "contents": [
                    "S > * 0.0.0.0/0 [1/0] via 192.168.10.1",
                    "C > * 192.168.10.0/24 is directly connected, port-channel0",
                ],
            },
        ],
        "total": 2,
    }
    mock_response = MockReponse(status_code=202, text=json.dumps(relust_data))
    mock_api = mocker.patch("pyfitel.cli.get", return_value=mock_response)
    url = "http://192.168.1.1:55443"

    res = get_commands_result(url=url, cli_id="1", bearer=True, token="testtoken")

    assert mock_api.call_count == 1
    assert res == relust_data


class TestExecCommands:
    def test_exec_commands_success(self, mocker: MockFixture):
        relust_data = {"clis_id": 1, "expires_in": 3600}
        mock_response = MockReponse(status_code=202, text=json.dumps(relust_data))
        mock_api = mocker.patch("pyfitel.cli.post", return_value=mock_response)

        url = "http://192.168.1.1:55443"
        cmd_list = [
            {"cmd": "show version", "on_fail": {"action": "exit"}},
            {"cmd": "show ip route", "on_fail": {"action": "continue"}},
        ]
        res = exec_commands(url=url, cmd_list=cmd_list, token="testtoken", bearer=True)

        assert mock_api.call_count == 1
        assert res == relust_data

    def test_exec_commands_failure(self, mocker: MockFixture):
        mock_response = MockReponse(status_code=202, text="foo")
        mock_api = mocker.patch("pyfitel.cli.post", return_value=mock_response)
        url = "http://192.168.1.1:55443"

        with pytest.raises(ValueError):
            exec_commands(url=url, cmd_list=[], token="testtoken", bearer=True)
        with pytest.raises(ValueError):
            exec_commands(
                url=url,
                cmd_list=[{"cmd": "show version", "on_fail": {"action": "exit"}}] * 11,
                token="testtoken",
                bearer=True,
            )
        assert mock_api.call_count == 0
