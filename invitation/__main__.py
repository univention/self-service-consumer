# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import asyncio
import logging
import sys
from aiohttp import (
    ClientError,
    ClientSession,
    ClientResponse,
    BasicAuth,
    ClientConnectorError,
    ClientTimeout,
)
from client import AsyncClient, MessageHandler, Settings
from shared.models import Message

from invitation.config import (
    Loglevel,
    SelfServiceConsumerSettings,
    get_selfservice_consumer_settings,
)


class InvalidMessageSchema(Exception):
    ...


class SelfServiceConsumer:
    MAX_RETRIES: int = 3

    def __init__(self, settings: SelfServiceConsumerSettings | None = None):
        self.settings = settings or get_selfservice_consumer_settings()
        self.logger = self.configure_logging(self.settings.log_level)

    @staticmethod
    def configure_logging(log_level: Loglevel) -> logging.Logger:
        console_handler = logging.StreamHandler(sys.stdout)
        logger = logging.getLogger("selfservice-invitation")
        logger.setLevel(log_level)
        formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d  %(name)-11s ( %(levelname)-7s ) : %(message)s",
            "%d.%m.%y %H:%M:%S",
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        return logger

    async def send_email(self, username: str) -> ClientResponse:
        async with ClientSession(
            timeout=ClientTimeout(total=30)
        ) as session, session.post(
            f"{self.settings.umc_server_url}/command/passwordreset/send_token",
            json={"options": {"username": username, "method": "email"}},
            auth=BasicAuth(
                self.settings.umc_admin_user, self.settings.umc_admin_password
            ),
        ) as response:
            return response

    async def send_email_invitation(self, username) -> bool:
        self.logger.info("Sending email invitation to user %s", username)
        try:
            response = await self.send_email(username)
        except ClientConnectorError as error:
            self.logger.error(
                "Failed to reach the UMC Server while trying to trigger an email invitation: %s",
                error,
            )
            return False
        except ClientError as error:
            self.logger.error(
                "Failed email invitation request: %s Check the UMC Server logs for more information.",
                error,
            )
            return False
        try:
            response_data = await response.json()
        except ClientError:
            self.logger.warning("Failed to parse the json response")
        else:
            self.logger.debug("UMC-Server response: %r", response_data)

        if response.status == 200:
            self.logger.info("Email invitation was triggered")
            return True

        self.logger.error(
            "There was an error requesting a user invitation email. UMC-Server status: %s",
            response.status,
        )
        return False

    def is_create_event(self, message: Message) -> bool:
        # TODO: use a better pydantic model for the message validation
        try:
            return message.body["new"] and not message.body["old"]
        except KeyError as error:
            # TODO: log the message ID
            self.logger.exception(
                "Invalid message body. Missing `new` and/or `old` object",
                exc_info=error,
            )
            raise InvalidMessageSchema()

    def needs_invitation_email(self, message: Message) -> bool:
        try:
            return all(
                (
                    message.body["new"]["properties"]["PasswordRecoveryEmail"],
                    message.body["new"]["properties"]["pwdChangeNextLogin"],
                )
            )
        except KeyError as error:
            # TODO: log the message ID
            self.logger.exception(
                "Invalid message body. "
                "Make sure that the selfservice udm extensions are installed in all necessary place.",
                exc_info=error,
            )
            raise InvalidMessageSchema()

    async def handle_user_event(self, message: Message) -> None:
        self.logger.debug("Received the message with the content: %s", message.body)

        if not self.is_create_event(message):
            self.logger.debug("Ignoring the message because it is not a create event.")
            return

        if not self.needs_invitation_email(message):
            self.logger.debug(
                "Ignoring the message because the user needs no invitation email."
            )
            return

        try:
            username = message.body["new"]["properties"]["username"]
        except KeyError as error:
            # TODO: log the message ID
            self.logger.exception(
                "Invalid message body. Missing `username` property in `new` object.",
                exc_info=error,
            )
            raise InvalidMessageSchema()

        for retries in range(self.settings.max_umc_request_retries + 1):
            if await self.send_email_invitation(username):
                return

            self.logger.info(
                "Failed sending the invitation email for username: %s. retries: %s",
                username,
                retries,
            )
            if retries != self.settings.max_umc_request_retries:
                timeout = min(2**retries / 10, 30)
                await asyncio.sleep(timeout)

        self.logger.error(
            "Maximum retries of %s reached for user %s. Check the UMC-Server logs for more information",
            self.settings.max_umc_request_retries,
            username,
        )
        # Crash the process; an unhandled message will be redelivered
        sys.exit(1)

    async def start_the_process_of_sending_invitations(
        self,
        provisionig_client: type[AsyncClient],
        message_handler: type[MessageHandler],
        provisioning_api_username: str,
    ) -> None:
        self.logger.info(
            "Starting the process of sending invitation emails via the UMC"
        )

        self.logger.info("Start listening for newly created users")
        async with provisionig_client() as client:
            await message_handler(
                client, provisioning_api_username, [self.handle_user_event]
            ).run()


def main() -> None:
    invitation = SelfServiceConsumer()
    provisioning_api_username = Settings().provisioning_api_username
    asyncio.run(
        invitation.start_the_process_of_sending_invitations(
            AsyncClient, MessageHandler, provisioning_api_username
        )
    )


if __name__ == "__main__":
    main()
