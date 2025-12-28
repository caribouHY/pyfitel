import json

from pytest_mock import MockFixture

from pyfitel import delete_token, publish_token

from .common import MockReponse


def test_publish_token_success(mocker: MockFixture):
    token_info = {
        "access_token": "1234567890abcdef1234567890abcdef",
        "token_type": "Bearer",
        "expires_in": 3600,
    }

    mock_api = mocker.patch(
        "pyfitel.token.post",
        return_value=MockReponse(status_code=201, text=json.dumps(token_info)),
    )

    url = "http://192.168.1.1:55443"
    user = "operator"
    password = "password123"

    result = publish_token(url=url, user=user, password=password)

    assert mock_api.call_count == 1
    assert result == token_info


def test_delete_token_success(mocker: MockFixture):
    mock_api = mocker.patch(
        "pyfitel.token.delete",
        return_value=MockReponse(status_code=204, text=""),
    )

    url = "http://192.168.1.1:55443"
    token = "1234567890abcdef1234567890abcdef"

    delete_token(url=url, token=token)
    assert mock_api.call_count == 1
