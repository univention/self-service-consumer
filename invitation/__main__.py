# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import asyncio
import logging
import os
import sys
from typing import Optional
from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientResponse,
    BasicAuth,
    ClientConnectorError,
)
from client import AsyncClient, MessageHandler, Settings
from shared.models import Message


class Invitation:
    MAX_RETRIES: int = 3

    def __init__(self):
        self.configure_logging()

        self.umc_server_url = os.environ.get("UMC_SERVER_URL", "http://umc-server")
        self.umc_admin_user = os.environ.get("UMC_ADMIN_USER", "admin")
        self.umc_admin_password = os.environ.get("UMC_ADMIN_PASSWORD")
        self.provisioning_admin_username = os.environ.get("PROVISIONING_ADMIN_USERNAME")
        self.provisioning_admin_password = os.environ.get("PROVISIONING_ADMIN_PASSWORD")
        self.provisioning_username = os.environ.get("PROVISIONING_USERNAME")
        self.provisioning_password = os.environ.get("PROVISIONING_PASSWORD")
        self.provisioning_api_base_url = os.environ.get("PROVISIONING_API_BASE_URL")
        self.provisioning_realm_topic = ["udm", "users/user"]

    def configure_logging(self) -> None:
        console_handler = logging.StreamHandler(sys.stdout)
        self.logger = logging.getLogger("selfservice-invitation")
        self.logger.setLevel(os.environ.get("LOG_LEVEL", "DEBUG"))
        formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d  %(name)-11s ( %(levelname)-7s ) : %(message)s",
            "%d.%m.%y %H:%M:%S",
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    @staticmethod
    def extract_username(msg: Message) -> Optional[str]:
        new_obj = msg.body.get("new")
        if new_obj and msg.body.get("old") is None:
            username = new_obj.get("uid")
            if (
                username
                and new_obj.get("univentionPasswordSelfServiceEmail")
                and (
                    new_obj.get("shadowMax") == 1
                    or new_obj.get("shadowLastChange") == 0
                )
            ):
                return username
        return None

    async def send_email(self, username: str) -> ClientResponse:
        async with ClientSession() as session, session.post(
            f"{self.umc_server_url}/command/passwordreset/send_token",
            json={"options": {"username": username, "method": "email"}},
            auth=BasicAuth(self.umc_admin_user, self.umc_admin_password),
        ) as response:
            return response

    async def retry_or_fail_sending_invitation(
        self, response_data: dict, username: str, retries: int
    ):
        self.logger.error(
            "There was an error requesting a user invitation email: %r",
            response_data,
        )
        self.logger.info(
            "Failed sending the invitation email for %s %s times",
            username,
            retries,
        )
        if retries < self.MAX_RETRIES:
            await asyncio.sleep(retries)
            return

        self.logger.error(
            "Maximum retries reached for user %s. Check the UMC logs for more information",
            username,
        )
        # Crash the process; an unhandled message will be redelivered
        sys.exit(1)

    async def handle_new_user(self, msg: Message) -> None:
        self.logger.info("Received the message with the content: %s", msg.body)
        username = self.extract_username(msg)
        if username is None:
            return

        try:
            retries = 1
            while True:
                self.logger.info("Sending email invitation to user %s", username)
                response = await self.send_email(username)
                response_data = await response.json()
                if response.status == 200:
                    self.logger.info("Email invitation was sent")
                    self.logger.debug(response_data)
                    return
                await self.retry_or_fail_sending_invitation(
                    response_data, username, retries
                )
                retries += 1

        except ClientConnectorError as e:
            self.logger.error("Could not reach UMC server: %r", e)
            raise

    async def start_the_process_of_sending_invitations(self) -> None:
        self.logger.info(
            "Starting the process of sending invitation emails via the UMC"
        )
        admin_settings = Settings(
            provisioning_api_username=self.provisioning_admin_username,
            provisioning_api_password=self.provisioning_admin_password,
            provisioning_api_base_url=self.provisioning_api_base_url,
        )
        settings = Settings(
            provisioning_api_username=self.provisioning_username,
            provisioning_api_password=self.provisioning_password,
            provisioning_api_base_url=self.provisioning_api_base_url,
        )
        async with AsyncClient(admin_settings) as admin_client:
            try:
                await admin_client.create_subscription(
                    settings.provisioning_api_username,
                    settings.provisioning_api_password,
                    [self.provisioning_realm_topic],
                    True,
                )
            except ClientResponseError as e:
                self.logger.warning("%s, Client already exists", e)

        self.logger.info("Listening for newly created users")
        async with AsyncClient(settings) as client:
            await MessageHandler(
                client, settings.provisioning_api_username, [self.handle_new_user]
            ).run()


def run() -> None:
    invitation = Invitation()
    asyncio.run(invitation.start_the_process_of_sending_invitations())


if __name__ == "__main__":
    run()
