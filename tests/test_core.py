import pytest
from pytest_mock import MockFixture
from requests.auth import HTTPBasicAuth

from pyfitel.core import FITELnetAPIError, auth, delete, get, patch, post, put

from .common import MockReponse


def test_auth_basic_success():
    user = "operator"
    password = "password123"

    result = auth(bearer=False, user=user, password=password, token=None)
    assert "auth" in result
    assert isinstance(result["auth"], HTTPBasicAuth)


def test_auth_bearer_success():
    token = "1234567890abcdef1234567890abcdef"
    result = auth(bearer=True, user=None, password=None, token=token)
    assert "headers" in result
    assert result["headers"]["Authorization"] == f"Bearer {token}"


def test_auth_basic_none():
    with pytest.raises(ValueError):
        auth(bearer=False, user="user", password=None, token=None)
    with pytest.raises(ValueError):
        auth(bearer=False, user=None, password="password", token=None)
    with pytest.raises(ValueError):
        auth(bearer=False, user=None, password=None, token=None)


def test_auth_bearer_none():
    with pytest.raises(ValueError):
        auth(bearer=True, user=None, password=None, token=None)


def test_get(mocker: MockFixture):
    mock_api = mocker.patch(
        "pyfitel.core.requests.get",
        return_value=MockReponse(status_code=200, text="success"),
    )

    url = "http://192.168.1.1:50443"
    res = get(base_url=url, endpoint="api", auth={"auth": "token"})
    assert mock_api.call_count == 1
    assert res.text == "success"


def test_post_success(mocker: MockFixture):
    mock_api = mocker.patch(
        "pyfitel.core.requests.post",
        return_value=MockReponse(status_code=200, text="success"),
    )

    url = "http://192.168.1.1:50443"
    res = post(base_url=url, endpoint="api", auth={"auth": "token"}, data={"data": "hoge"})
    assert mock_api.call_count == 1
    assert res.text == "success"


def test_post_failure(mocker: MockFixture):
    mock_api = mocker.patch(
        "pyfitel.core.requests.post",
        return_value=MockReponse(status_code=400, text='{"error": "error"}'),
    )

    url = "http://192.168.1.1:50443"
    with pytest.raises(FITELnetAPIError):
        post(base_url=url, endpoint="api", auth={"auth": "token"}, data={"data": "hoge"})
    assert mock_api.call_count == 1


def test_delete(mocker: MockFixture):
    mock_api = mocker.patch(
        "pyfitel.core.requests.delete",
        return_value=MockReponse(status_code=200, text="deleted"),
    )

    url = "http://192.168.1.1:50443"
    delete(base_url=url, endpoint="api", auth={"auth": "token"})
    assert mock_api.call_count == 1


def test_put(mocker: MockFixture):
    mock_api = mocker.patch(
        "pyfitel.core.requests.put",
        return_value=MockReponse(status_code=200, text="ok"),
    )
    url = "http://192.168.1.1:50443"
    put(base_url=url, endpoint="api", auth=auth(bearer=True, token="testtoken", user=None, password=None), data=b"data")
    assert mock_api.call_count == 1


def test_patch(mocker: MockFixture):
    mock_api = mocker.patch(
        "pyfitel.core.requests.patch",
        return_value=MockReponse(status_code=200, text="ok"),
    )
    url = "http://192.168.1.1:50443"
    patch(
        base_url=url, endpoint="api", auth=auth(bearer=True, token="testtoken", user=None, password=None), data=b"data"
    )
    assert mock_api.call_count == 1
