# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import asyncio
import logging
import sys
from importlib.metadata import version
from typing import Awaitable, Callable

from aiohttp import (
    BasicAuth,
    ClientConnectorError,
    ClientError,
    ClientResponse,
    ClientSession,
    ClientTimeout,
)

from invitation.config import (
    Loglevel,
    SelfServiceConsumerSettings,
    get_selfservice_consumer_settings,
)
from univention.provisioning.consumer import MessageHandler, ProvisioningConsumerClient
from univention.provisioning.models import Body, Message

LOG_FORMAT = "%(asctime)s %(levelname)-5s [%(module)s.%(funcName)s:%(lineno)d] %(message)s"

logger = logging.getLogger(__name__)


class InvalidMessageSchema(Exception): ...


class SelfServiceConsumer:
    def __init__(self, settings: SelfServiceConsumerSettings | None = None):
        self.settings = settings or get_selfservice_consumer_settings()

    async def send_email(self, username: str) -> ClientResponse:
        session_kwargs = {
            "url": f"{self.settings.umc_server_url}/command/passwordreset/send_token",
            "json": {"options": {"username": username, "method": "email"}},
            "auth": BasicAuth(self.settings.umc_admin_user, self.settings.umc_admin_password),
        }
        async with (
            ClientSession(timeout=ClientTimeout(total=30)) as session,
            session.post(**session_kwargs) as response,
        ):
            return response

    async def send_email_invitation(self, username) -> bool:
        logger.info("Sending email invitation to user %r", username)
        try:
            response = await self.send_email(username)
        except ClientConnectorError as error:
            logger.error(
                "Failed to reach the UMC Server while trying to trigger an email invitation: %s",
                error,
            )
            return False
        except ClientError as error:
            logger.error(
                "Failed email invitation request: %s Check the UMC Server logs for more information.",
                error,
            )
            return False
        try:
            response_data = await response.json()
        except ClientError:
            logger.warning("Failed to parse the json response")
        else:
            logger.debug("UMC-Server response: %r", response_data)

        if response.status == 200:
            logger.info("Email invitation was triggered")
            return True

        logger.error(
            "There was an error requesting a user invitation email. UMC-Server status: %d",
            response.status,
        )
        return False

    @staticmethod
    def is_create_event(message_body: Body) -> bool:
        return message_body.new and not message_body.old

    @staticmethod
    def needs_invitation_email(message_body: Body) -> bool:
        try:
            return all(
                (
                    message_body.new["properties"]["PasswordRecoveryEmail"],
                    message_body.new["properties"]["pwdChangeNextLogin"],
                )
            )
        except KeyError:
            # TODO: log the message ID
            raise InvalidMessageSchema(
                "Invalid message body. "
                "Make sure that the selfservice udm extensions are installed in all necessary place.",
            )

    async def handle_user_event(self, message: Message) -> None:
        message_body = message.body
        logger.debug("Received the message with the content: %s", message_body)

        if not self.is_create_event(message_body):
            logger.debug("Ignoring the message because it is not a create event.")
            return

        if not self.needs_invitation_email(message_body):
            logger.debug("Ignoring the message because the user needs no invitation email.")
            return

        try:
            username = message_body.new["properties"]["username"]
        except KeyError:
            # TODO: log the message ID
            raise InvalidMessageSchema("Invalid message body. Missing `username` property in `new` object.")

        for retries in range(self.settings.max_umc_request_retries + 1):
            if await self.send_email_invitation(username):
                return

            logger.debug(
                "Failed sending the invitation email for username: %r. retries: %d",
                username,
                retries,
            )
            if retries != self.settings.max_umc_request_retries:
                timeout = min(2**retries / 10, 30)
                await asyncio.sleep(timeout)

        logger.error(
            "Maximum retries of %d reached for user %r. Check the UMC-Server logs for more information.",
            self.settings.max_umc_request_retries,
            username,
        )
        # Crash the process; an unhandled message will be redelivered
        sys.exit(1)


def configure_logging(log_level: Loglevel) -> None:
    _handler = logging.StreamHandler(sys.stdout)
    _logger = logging.getLogger()
    _logger.setLevel(log_level)
    formatter = logging.Formatter(LOG_FORMAT)
    _handler.setFormatter(formatter)
    _logger.addHandler(_handler)


async def start_consumer(
    provisioning_client: type[ProvisioningConsumerClient],
    message_handler: type[MessageHandler],
    handler: Callable[[Message], Awaitable[None]],
) -> None:
    logger.info("Starting to listen for newly created users for sending of invitation emails via the UMC.")
    logger.info("Using 'nubus-provisioning-consumer' library version %r.", version("nubus-provisioning-consumer"))
    async with provisioning_client() as client:
        await message_handler(client, [handler]).run()


if __name__ == "__main__":
    _settings = get_selfservice_consumer_settings()
    configure_logging(_settings.log_level)
    invitation = SelfServiceConsumer()
    asyncio.run(start_consumer(ProvisioningConsumerClient, MessageHandler, invitation.handle_user_event))
