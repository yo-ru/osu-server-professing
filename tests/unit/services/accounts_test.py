import pytest_mock

from server.services import accounts
from testing import sample_data


async def test_should_create_account(
    mocker: pytest_mock.MockerFixture,
):
    # arrange
    fake_account = sample_data.fake_account()
    mocker.patch(
        "server.repositories.accounts.create",
        return_value=fake_account,
    )

    # act
    account = await accounts.create(
        username=fake_account["username"],
        email_address=fake_account["email_address"],
        privileges=fake_account["privileges"],
        password=fake_account["password"],
        country=fake_account["country"],
    )

    # assert
    assert account == fake_account


async def test_should_fetch_many_accounts(
    mocker: pytest_mock.MockerFixture,
):
    # arrange
    fake_accounts = [
        sample_data.fake_account(),
        sample_data.fake_account(),
        sample_data.fake_account(),
    ]
    mocker.patch(
        "server.repositories.accounts.fetch_many",
        return_value=fake_accounts,
    )

    # act
    accounts_ = await accounts.fetch_many()

    # assert
    assert accounts_ == fake_accounts


async def test_should_create_account_with_invalid_username(
    mocker: pytest_mock.MockerFixture,
):
    # arrange
    mocker.patch(
        "server.validation.validate_username",
        return_value=False,
    )

    # act
    account = await accounts.create(
        username="",
        email_address="",
        privileges=0,
        password="",
        country="",
    )

    # assert
    assert account == accounts.ServiceError.ACCOUNTS_USERNAME_INVALID
