from copy import deepcopy
from datetime import datetime
from unittest.mock import AsyncMock, patch, MagicMock
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


UID = "testuser"
MESSAGE = Message(
    publisher_name=PublisherName.udm_listener,
    ts=datetime(2023, 11, 9, 11, 15, 52, 616061),
    realm="udm",
    topic="users/user",
    body={
        "new": {
            "uid": UID,
            "univentionPasswordSelfServiceEmail": "example@gmail.com",
            "shadowMax": 1,
        },
        "old": None,
    },
)
MESSAGE_OLD_USER = deepcopy(MESSAGE)
MESSAGE_OLD_USER.body = {"new": {"uid": UID}, "old": {"uid": UID}}

MESSAGE_NO_EMAIL = deepcopy(MESSAGE)
MESSAGE_NO_EMAIL.body = {"new": {"uid": UID, "shadowMax": 1}, "old": None}

MESSAGE_INVALID_SHADOWMAX_VALUES = deepcopy(MESSAGE)
MESSAGE_INVALID_SHADOWMAX_VALUES.body = {
    "new": {
        "uid": UID,
        "univentionPasswordSelfServiceEmail": "example@gmail.com",
        "shadowMax": 0,
        "shadowLastChange": 1,
    },
    "old": None,
}

MESSAGE_NO_UID = deepcopy(MESSAGE)
MESSAGE_NO_UID.body = {
    "new": {
        "univentionPasswordSelfServiceEmail": "example@gmail.com",
    },
    "old": None,
}


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
def async_client() -> AsyncMock:
    yield patch(
        "invitation.__main__.AsyncClient"
    ).start().return_value.__aenter__.return_value


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
            return_value=invitation.handle_new_user(MESSAGE)
        )

        await invitation.start_the_process_of_sending_invitations()

        async_client.create_subscription.assert_called_once_with(
            ENV_DEFAULTS["PROVISIONING_USERNAME"],
            ENV_DEFAULTS["PROVISIONING_PASSWORD"],
            [["udm", "users/user"]],
            True,
        )
        message_handler.run.assert_called_once_with()
        mock_post.assert_called_once_with(
            f"{ENV_DEFAULTS['UMC_SERVER_URL']}/command/passwordreset/send_token",
            json={"options": {"username": UID, "method": "email"}},
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
            return_value=invitation.handle_new_user(MESSAGE_OLD_USER)
        )

        await invitation.start_the_process_of_sending_invitations()

        async_client.create_subscription.assert_called_once_with(
            ENV_DEFAULTS["PROVISIONING_USERNAME"],
            ENV_DEFAULTS["PROVISIONING_PASSWORD"],
            [["udm", "users/user"]],
            True,
        )
        message_handler.run.assert_called_once_with()
        mock_post.assert_not_called()

    @pytest.mark.parametrize(
        "message", [MESSAGE_NO_EMAIL, MESSAGE_NO_UID, MESSAGE_INVALID_SHADOWMAX_VALUES]
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
            return_value=invitation.handle_new_user(message)
        )

        await invitation.start_the_process_of_sending_invitations()

        async_client.create_subscription.assert_called_once_with(
            ENV_DEFAULTS["PROVISIONING_USERNAME"],
            ENV_DEFAULTS["PROVISIONING_PASSWORD"],
            [["udm", "users/user"]],
            True,
        )
        message_handler.run.assert_called_once_with()
        mock_post.assert_not_called()

    @patch("invitation.__main__.asyncio.sleep")
    async def test_error_during_sending_email(
        self,
        mock_sleep,
        mock_post,
        async_client: AsyncClient,
        message_handler: MessageHandler,
    ):
        invitation = Invitation()
        mock_post.return_value.__aenter__.return_value = MockedResponse(500, {})
        message_handler.run = AsyncMock(
            return_value=invitation.handle_new_user(MESSAGE)
        )
        with pytest.raises(SystemExit, match="1"):
            await invitation.start_the_process_of_sending_invitations()

        async_client.create_subscription.assert_called_once_with(
            ENV_DEFAULTS["PROVISIONING_USERNAME"],
            ENV_DEFAULTS["PROVISIONING_PASSWORD"],
            [["udm", "users/user"]],
            True,
        )
        message_handler.run.assert_called_once_with()
        assert mock_post.call_count == 3
        assert mock_sleep.call_count == 2
