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
from univention.provisioning.consumer import MessageHandler, ProvisioningConsumerClient
from univention.provisioning.models import Message, Body

from invitation.config import (
    Loglevel,
    SelfServiceConsumerSettings,
    get_selfservice_consumer_settings,
)


class InvalidMessageSchema(Exception):
    ...


class SelfServiceConsumer:
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

    @staticmethod
    def is_create_event(message_body: Body) -> bool:
        return message_body.new and not message_body.old

    def needs_invitation_email(self, message_body: Body) -> bool:
        try:
            return all(
                (
                    message_body.new["properties"]["PasswordRecoveryEmail"],
                    message_body.new["properties"]["pwdChangeNextLogin"],
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
        message_body = message.body
        self.logger.debug("Received the message with the content: %s", message_body)

        if not self.is_create_event(message_body):
            self.logger.debug("Ignoring the message because it is not a create event.")
            return

        if not self.needs_invitation_email(message_body):
            self.logger.debug(
                "Ignoring the message because the user needs no invitation email."
            )
            return

        try:
            username = message_body.new["properties"]["username"]
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
        provisioning_client: type[ProvisioningConsumerClient],
        message_handler: type[MessageHandler],
    ) -> None:
        self.logger.info(
            "Starting the process of sending invitation emails via the UMC"
        )

        self.logger.info("Start listening for newly created users")
        async with provisioning_client() as client:
            await message_handler(client, [self.handle_user_event]).run()


def main() -> None:
    invitation = SelfServiceConsumer()
    asyncio.run(
        invitation.start_the_process_of_sending_invitations(
            ProvisioningConsumerClient, MessageHandler
        )
    )


if __name__ == "__main__":
    main()
