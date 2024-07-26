# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

from copy import deepcopy
from datetime import datetime
from unittest.mock import AsyncMock, patch, MagicMock, Mock, call
import pytest
from client import AsyncClient, MessageHandler
from shared.models import Message, PublisherName
from aiohttp import BasicAuth
from invitation.__main__ import Invitation
from tests import set_test_env_vars, ENV_DEFAULTS

set_test_env_vars()


class AsyncContextManagerMock(MagicMock):
    async def __aenter__(self):
        return self.aenter()

    async def __aexit__(self, *args):
        pass


class MockedResponse(MagicMock):
    def __init__(self, status, json=None, *args):
        super().__init__(*args)
        self.status = status
        self.json = AsyncMock(return_value=json)


USERNAME = "testuser"
MESSAGE = Message(
    publisher_name=PublisherName.udm_listener,
    ts=datetime(2023, 11, 9, 11, 15, 52, 616061),
    realm="udm",
    topic="users/user",
    body={
        "new": {
            "properties": {
                "username": USERNAME,
                "PasswordRecoveryEmail": "example@gmail.com",
                "pwdChangeNextLogin": True,
            }
        },
        "old": None,
    },
)
MESSAGE_OLD_USER = deepcopy(MESSAGE)
MESSAGE_OLD_USER.body["old"] = {"properties": {"username": USERNAME}}

MESSAGE_NO_EMAIL = deepcopy(MESSAGE)
MESSAGE_NO_EMAIL.body["new"]["properties"] = {
    "username": USERNAME,
    "pwdChangeNextLogin": True,
}

MESSAGE_PWD_CHANGE_NEXT_LOGIN_IS_NONE = deepcopy(MESSAGE)
MESSAGE_PWD_CHANGE_NEXT_LOGIN_IS_NONE.body["new"]["properties"] = {
    "username": USERNAME,
    "PasswordRecoveryEmail": "example@gmail.com",
    "pwdChangeNextLogin": None,
}

MESSAGE_NO_USERNAME = deepcopy(MESSAGE)
MESSAGE_NO_USERNAME.body["new"]["properties"] = {
    "PasswordRecoveryEmail": "example@gmail.com",
    "pwdChangeNextLogin": True,
}


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
def async_client() -> AsyncMock:
    yield patch("invitation.__main__.AsyncClient").start()


@pytest.fixture
def message_handler() -> AsyncMock:
    yield patch("invitation.__main__.MessageHandler").start().return_value


@pytest.mark.anyio
@patch("invitation.__main__.ClientSession.post", new_callable=AsyncContextManagerMock)
class TestInvitation:
    async def test_send_email_successfully(
        self, mock_post, async_client: AsyncClient, message_handler: MessageHandler
    ):
        invitation = Invitation()
        mock_post.return_value.__aenter__.return_value = MockedResponse(200, {})
        message_handler.run = AsyncMock(
            side_effect=await invitation.handle_new_user(MESSAGE)
        )

        await invitation.start_the_process_of_sending_invitations()

        async_client.assert_called_once_with()
        message_handler.run.assert_called_once_with()
        mock_post.assert_called_once_with(
            f"{ENV_DEFAULTS['UMC_SERVER_URL']}/command/passwordreset/send_token",
            json={"options": {"username": USERNAME, "method": "email"}},
            auth=BasicAuth(
                ENV_DEFAULTS["UMC_ADMIN_USER"], ENV_DEFAULTS["UMC_ADMIN_PASSWORD"]
            ),
        )

    async def test_old_user(
        self, mock_post, async_client: AsyncClient, message_handler: MessageHandler
    ):
        invitation = Invitation()
        mock_post.return_value.__aenter__.return_value = MockedResponse(200, {})
        message_handler.run = AsyncMock(
            side_effect=await invitation.handle_new_user(MESSAGE_OLD_USER)
        )

        await invitation.start_the_process_of_sending_invitations()

        async_client.assert_called_once_with()
        message_handler.run.assert_called_once_with()
        mock_post.assert_not_called()

    @pytest.mark.parametrize(
        "message",
        [MESSAGE_NO_EMAIL, MESSAGE_NO_USERNAME, MESSAGE_PWD_CHANGE_NEXT_LOGIN_IS_NONE],
    )
    async def test_user_does_not_have_needed_fields(
        self,
        mock_post,
        message,
        async_client: AsyncClient,
        message_handler: MessageHandler,
    ):
        invitation = Invitation()
        mock_post.return_value.__aenter__.return_value = MockedResponse(200, {})
        message_handler.run = AsyncMock(
            side_effect=await invitation.handle_new_user(message)
        )

        await invitation.start_the_process_of_sending_invitations()

        async_client.assert_called_once_with()
        message_handler.run.assert_called_once_with()
        mock_post.assert_not_called()

    @patch("invitation.__main__.asyncio.sleep")
    @patch("invitation.__main__.sys.exit")
    async def test_error_during_sending_email(
        self,
        mock_sys_exit,
        mock_sleep,
        mock_post,
        async_client: AsyncClient,
        message_handler: MessageHandler,
    ):
        invitation = Invitation()
        mock_sys_exit.side_effect = Exception("SystemExit 1")
        mock_post.return_value.__aenter__.return_value = MockedResponse(500, {})
        message_handler.run = Mock(return_value=invitation.handle_new_user(MESSAGE))
        with pytest.raises(Exception, match="SystemExit 1"):
            await invitation.start_the_process_of_sending_invitations()

        async_client.assert_called_once_with()
        message_handler.run.assert_called_once_with()
        assert mock_post.call_count == 3
        mock_sleep.assert_has_calls([call(2), call(4)])
        mock_sys_exit.assert_called_once_with(1)
