# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

from copy import deepcopy
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from aiohttp import BasicAuth

from invitation.__main__ import start_consumer
from invitation.config import SelfServiceConsumerSettings
from invitation.consumer import InvalidMessageSchema, SelfServiceConsumer
from univention.provisioning.consumer import (
    MessageHandler,
    ProvisioningConsumerClient,
    ProvisioningConsumerClientSettings,
)
from univention.provisioning.consumer.config import MessageHandlerSettings
from univention.provisioning.models import (
    Body,
    ProvisioningMessage,
    PublisherName,
)


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
DN = f"uid={USERNAME},cn=users,dc=univention-organization,dc=intranet"
MESSAGE = ProvisioningMessage(
    publisher_name=PublisherName.udm_listener,
    ts=datetime.now(),
    realm="udm",
    topic="users/user",
    body=Body(
        old={},
        new={
            "dn": DN,
            "properties": {
                "username": USERNAME,
                "pwdChangeNextLogin": True,
                "PasswordRecoveryEmail": "lohmer@univention.de",
            },
        },
    ),
    sequence_number=1,
    num_delivered=1,
)

MESSAGE_OLD_USER = deepcopy(MESSAGE)
MESSAGE_OLD_USER.body.old = {"dn": DN, "properties": {"username": USERNAME}}

MESSAGE_NO_EMAIL = deepcopy(MESSAGE)
MESSAGE_NO_EMAIL.body.new["properties"] = {
    "username": USERNAME,
    "pwdChangeNextLogin": True,
}

MESSAGE_PWD_CHANGE_NEXT_LOGIN_IS_NONE = deepcopy(MESSAGE)
MESSAGE_PWD_CHANGE_NEXT_LOGIN_IS_NONE.body.new["properties"] = {
    "username": USERNAME,
    "PasswordRecoveryEmail": "lohmer@univention.de",
    "pwdChangeNextLogin": None,
}

MESSAGE_NO_USERNAME = deepcopy(MESSAGE)
MESSAGE_NO_USERNAME.body.new["properties"] = {
    "PasswordRecoveryEmail": "lohmer@univention.de",
    "pwdChangeNextLogin": True,
}


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture
def selfservice_consumer_settings() -> SelfServiceConsumerSettings:
    return SelfServiceConsumerSettings(
        log_level="DEBUG",
        max_umc_request_retries=3,
        umc_server_url="http://foo.local",
        umc_admin_user="user",
        umc_admin_password="password",
    )


@pytest.fixture
def selfservice_consumer(selfservice_consumer_settings) -> SelfServiceConsumer:
    return SelfServiceConsumer(settings=selfservice_consumer_settings)


@pytest.fixture
def provisioining_client_settings() -> ProvisioningConsumerClientSettings:
    return ProvisioningConsumerClientSettings(
        provisioning_api_base_url="http://foo.local",
        provisioning_api_username="bar",
        provisioning_api_password="baz",
        log_level="DEBUG",
    )


@pytest.fixture
def message_handler_settings() -> MessageHandlerSettings:
    return MessageHandlerSettings(max_acknowledgement_retries=3)


@pytest.fixture
async def mock_provisioning_client(
    provisioining_client_settings: ProvisioningConsumerClientSettings,
) -> ProvisioningConsumerClient:
    client = ProvisioningConsumerClient(provisioining_client_settings)
    client.get_subscription_message = AsyncMock()
    client.set_message_status = AsyncMock()
    return client


@pytest.fixture
async def mock_message_handler(
    message_handler_settings: MessageHandlerSettings,
    mock_provisioning_client: ProvisioningConsumerClient,
    selfservice_consumer,
) -> MessageHandler:
    return MessageHandler(
        mock_provisioning_client,
        [selfservice_consumer.handle_user_event],
        message_handler_settings,
    )


def mock_constructor_factory(instance):
    def mock_constructor(*args):
        return instance

    return mock_constructor


class EscapeLoopException(Exception): ...


@pytest.mark.xfail(reason="Expected failure due to known issue with debug_msg in nubus-provisioning-consumer library.")
@pytest.mark.anyio
async def test_invalid_requests(
    selfservice_consumer: SelfServiceConsumer,
    mock_provisioning_client: ProvisioningConsumerClient,
    mock_message_handler: MessageHandler,
):
    invalid_message = deepcopy(MESSAGE)
    invalid_message.body.old = {}
    invalid_message.body.new = {}
    mock_provisioning_client.get_subscription_message.side_effect = [
        invalid_message,
        EscapeLoopException("let's exit the loop"),
    ]

    selfservice_consumer.send_email_invitation = AsyncMock()

    with pytest.raises(EscapeLoopException):
        await start_consumer(
            mock_constructor_factory(mock_provisioning_client),
            mock_constructor_factory(mock_message_handler),
            selfservice_consumer.handle_user_event,
        )

    selfservice_consumer.send_email_invitation.assert_not_awaited()


@pytest.mark.anyio
async def test_valid_provisioning_message(
    selfservice_consumer: SelfServiceConsumer,
    mock_provisioning_client: ProvisioningConsumerClient,
    mock_message_handler: MessageHandler,
):
    mock_provisioning_client.get_subscription_message.side_effect = [
        MESSAGE,
        EscapeLoopException("let's exit the loop"),
    ]

    selfservice_consumer.send_email_invitation = AsyncMock()

    with pytest.raises(EscapeLoopException):
        await start_consumer(
            mock_constructor_factory(mock_provisioning_client),
            mock_constructor_factory(mock_message_handler),
            selfservice_consumer.handle_user_event,
        )
    selfservice_consumer.send_email_invitation.assert_awaited_once_with("testuser")


@pytest.mark.anyio
async def test_send_email(
    selfservice_consumer: SelfServiceConsumer,
    selfservice_consumer_settings: SelfServiceConsumerSettings,
):
    mock_post = AsyncMock()
    mock_post.__aenter__.return_value = MockedResponse(200, {})

    # Mock for the context manager that will be used inside the outer context manager
    mock_post_cm = Mock(return_value=mock_post)

    meta = AsyncMock()
    meta.post = mock_post_cm

    client_session_instance = AsyncMock()
    client_session_instance.__aenter__.return_value = meta
    client_session = Mock(return_value=client_session_instance)

    with patch("invitation.consumer.ClientSession", client_session):
        await selfservice_consumer.send_email(USERNAME)

    mock_post_cm.assert_called_once_with(
        url=f"{selfservice_consumer_settings.umc_server_url}/command/passwordreset/send_token",
        json={"options": {"username": USERNAME, "method": "email", "is_invitation": True}},
        auth=BasicAuth(
            selfservice_consumer_settings.umc_admin_user,
            selfservice_consumer_settings.umc_admin_password,
        ),
    )
    mock_post.__aenter__.assert_called_once()


@pytest.mark.anyio
@pytest.mark.parametrize(
    "message",
    [MESSAGE_OLD_USER, MESSAGE_PWD_CHANGE_NEXT_LOGIN_IS_NONE],
)
async def test_message_filtering(
    message: ProvisioningMessage,
    selfservice_consumer: SelfServiceConsumer,
):
    selfservice_consumer.send_email_invitation = AsyncMock()

    await selfservice_consumer.handle_user_event(message)

    selfservice_consumer.send_email_invitation.assert_not_awaited()


@pytest.mark.anyio
@pytest.mark.parametrize(
    "message",
    [MESSAGE_NO_EMAIL, MESSAGE_NO_USERNAME],
)
async def test_invalid_message_schema(
    message: ProvisioningMessage,
    selfservice_consumer: SelfServiceConsumer,
):
    selfservice_consumer.send_email_invitation = AsyncMock()

    with pytest.raises(InvalidMessageSchema):
        await selfservice_consumer.handle_user_event(message)

    selfservice_consumer.send_email_invitation.assert_not_awaited()


@pytest.mark.anyio
@patch("asyncio.sleep", return_value=None)
@pytest.mark.parametrize("retries", [0, 3, 9, 10])
async def test_valid_retry_values(mock_sleep, retries, selfservice_consumer: SelfServiceConsumer):
    selfservice_consumer.settings.max_umc_request_retries = retries
    selfservice_consumer.send_email_invitation = AsyncMock(return_value=False)

    with pytest.raises(SystemExit) as excinfo:
        await selfservice_consumer.handle_user_event(MESSAGE)

    assert excinfo.value.code == 1
    assert selfservice_consumer.send_email_invitation.call_count == retries + 1
    assert mock_sleep.call_count == retries
