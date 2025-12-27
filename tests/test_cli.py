import pytest
from pytest_mock import MockFixture

from pyfitel import FITELnetAPIError, exec_command

from .common import MockReponse


class TestExecCommand:
    def test_exec_command_basic_success(self, mocker: MockFixture):
        command_result = """
    --------------------- present-side ---------------------
    F70   Version 01.16(01)[0]00.00.0 [2025/11/06 15:00]

    ---------------------- other-side ----------------------
    F70   Version 01.08(00)b0[0]00.00.0 [2023/06/30 15:00]
    """
        mock_api = mocker.patch(
            "pyfitel.cli.requests.post",
            return_value=MockReponse(status_code=201, text=command_result),
        )

        url = "http://192.168.1.1:55443"
        cmd = "show version"
        user = "operator"
        password = "password123"

        result = exec_command(
            url=url, cmd=cmd, user=user, password=password, bearer=False
        )

        assert mock_api.call_count == 1
        assert result == command_result

    def test_exec_command_bearer_success(self, mocker: MockFixture):
        command_result = """
    --------------------- present-side ---------------------
    F70   Version 01.16(01)[0]00.00.0 [2025/11/06 15:00]

    ---------------------- other-side ----------------------
    F70   Version 01.08(00)b0[0]00.00.0 [2023/06/30 15:00]
    """
        mock_api = mocker.patch(
            "pyfitel.cli.requests.post",
            return_value=MockReponse(status_code=201, text=command_result),
        )

        url = "http://192.168.1.1:55443"
        cmd = "show version"
        token = "abcdefg1234567"

        result = exec_command(url=url, cmd=cmd, token=token, bearer=True)

        assert mock_api.call_count == 1
        assert result == command_result

    def test_exec_command_basic_none(self, mocker: MockFixture):
        url = "http://192.168.1.1:55443"
        cmd = "show version"

        with pytest.raises(ValueError):
            exec_command(url=url, cmd=cmd, user=None, password=None, bearer=False)

    def test_exec_command_bearer_none(self, mocker: MockFixture):
        url = "http://192.168.1.1:55443"
        cmd = "show version"

        with pytest.raises(ValueError):
            exec_command(url=url, cmd=cmd, token=None, bearer=True)

    def test_exec_command_api_error(self, mocker: MockFixture):
        return_value = MockReponse(status_code=401, text='{"error": "Unauthorized"}')
        mock_api = mocker.patch("pyfitel.cli.requests.post", return_value=return_value)
        url = "http://192.168.1.1:55443"
        cmd = "show version"

        with pytest.raises(FITELnetAPIError):
            exec_command(url=url, cmd=cmd, token="testtoken", bearer=True)
        assert mock_api.call_count == 1
