# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH
import asyncio
import logging
import os
import sys
from typing import Optional
from aiohttp import ClientResponseError
import requests
from client import AsyncClient, MessageHandler, Settings
from shared.models import Message


class Invitation():

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

        self.retry_cache = {}

    def configure_logging(self):
        console_handler = logging.StreamHandler(sys.stdout)
        self.logger = logging.getLogger("selfservice-invitation")
        self.logger.setLevel(os.environ.get("LOG_LEVEL", "DEBUG"))
        formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d  %(name)-11s ( %(levelname)-7s ) : %(message)s",
            "%d.%m.%y %H:%M:%S",
        )
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def evaluate_retry(self, username: str):
        retries = self.retry_cache.get(username, 0)
        if retries > 4:
            self.logger.error("Maximum retries reached for user %s. Check the UMC logs for more information", username)
            self.logger.debug("User retries are %r", self.retry_cache)
            sys.exit(1)

        retries += 1
        self.retry_cache[username] = retries
        self.logger.debug("Tried sending the invitation email for %s %s times", username, retries)

    @staticmethod
    def extract_username(msg: Message) -> Optional[str]:
        new_obj = msg.body.get("new")
        if new_obj and msg.body.get("old") is None:
            username = new_obj.get("uid")
            if username and new_obj.get("univentionPasswordSelfServiceEmail"):
                return username
        return None

    def send_email(self, username: str):
        return requests.post(
            f"{self.umc_server_url}/command/passwordreset/send_token",
            json={
                "options": {
                    "username": username,
                    "method": "email",
                },
            },
            auth=(self.umc_admin_user, self.umc_admin_password),
        )

    async def handle_new_user(self, msg: Message):
        self.logger.info("Received the message with the content: %s", msg.body)
        username = self.extract_username(msg)
        if username is None:
            return

        try:
            retries = 0
            while retries < 3:
                self.logger.info("Sending email invitation to user %s" % username)
                response = self.send_email(username)
                response_data = response.json()
                if response.status_code != 200:
                    self.logger.error(
                        "There was an error requesting a user invitation email: %r"
                        % response_data
                    )
                    retries += 1
                    self.logger.info("Tried sending the invitation email for %s %s times", username, retries)
                    continue
                self.logger.info("Email invitation was sent")
                self.logger.debug(response_data)
                return

            self.logger.error("Maximum retries reached for user %s. Check the UMC logs for more information", username)
            sys.exit(1)

        except requests.exceptions.ConnectionError as e:
            self.logger.error("Could not reach UMC server: %r" % e)

    async def run(self):
        self.logger.info("Starting the process of sending invitation emails via the UMC")
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


if __name__ == "__main__":
    invitation = Invitation()
    asyncio.run(invitation.run())
