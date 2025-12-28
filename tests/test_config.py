from pytest_mock import MockFixture

from pyfitel import replace_config, update_config

from .common import MockReponse


def test_replace_confgi(mocker: MockFixture):
    mock_api = mocker.patch(
        "pyfitel.config.put",
        return_value=MockReponse(status_code=200, text=""),
    )

    url = "http://192.168.1.1:50443"
    token = "1234567890abcdef1234567890abcdef"
    config = """
    int lo 1
    description foobar
    """
    replace_config(url=url, config=config, bearer=True, token=token)
    assert mock_api.call_count == 1


def test_update_confgi(mocker: MockFixture):
    mock_api = mocker.patch(
        "pyfitel.config.patch",
        return_value=MockReponse(status_code=200, text=""),
    )

    url = "http://192.168.1.1:50443"
    token = "1234567890abcdef1234567890abcdef"
    config = """
    int lo 1
    description foobar
    """
    update_config(url=url, config=config, bearer=True, token=token)
    assert mock_api.call_count == 1
