# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import asyncio
import logging
import sys

from aiohttp import (
    ClientConnectorError,
    ClientError,
    ClientResponse,
    ClientSession,
    ClientTimeout,
)

from invitation.config import SelfServiceConsumerSettings, get_selfservice_consumer_settings
from univention.provisioning.models import Body, ProvisioningMessage

logger = logging.getLogger(__name__)


class InvalidMessageSchema(Exception): ...


class SelfServiceConsumer:
    def __init__(self, settings: SelfServiceConsumerSettings | None = None):
        self.settings = settings or get_selfservice_consumer_settings()

    async def send_email(self, username: str) -> ClientResponse:
        session_kwargs = {
            "url": f"{self.settings.umc_server_url}/command/passwordreset/send_token",
            "json": {"options": {"username": username, "method": "email", "is_invitation": True}},
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

    async def handle_user_event(self, message: ProvisioningMessage) -> None:
        message_body = message.body
        logger.info(
            "Received message with topic: %s, sequence_number: %d, num_delivered: %d",
            message.topic,
            message.sequence_number,
            message.num_delivered,
        )
        logger.debug("Message body: %r", message_body)

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
