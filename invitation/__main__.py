import logging
import os
import sys
import time
from pathlib import Path

import requests


class Invitation():

    def __init__(self):
        self.configure_logging()

        self.umc_server_url = os.environ.get("UMC_SERVER_URL", "http://umc-server")
        self.umc_admin_user = os.environ.get("UMC_ADMIN_USER", "admin")
        self.umc_admin_password = os.environ.get("UMC_ADMIN_PASSWORD")
        self.queue_directory = Path("/var/cache/listener")

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

    def handle_file(self, path: Path):
        username = path.name[:-5]
        try:
            response = requests.post(
                f"{self.umc_server_url}/command/passwordreset/send_token",
                json={
                    "options": {
                        "username": username,
                        "method": "email",
                    },
                },
                auth=(self.umc_admin_user, self.umc_admin_password),
            )
            response_data = response.json()
            if response.status_code != 200:
                self.logger.error(
                    "There was an error requesting a user invitation email: %r"
                    % response_data
                )
                self.evaluate_retry(username)
                return
            self.logger.info("Email invitation sent to user %s" % username)
            self.logger.debug(response_data)
            os.remove(path)
            self.logger.debug("Removing %s to avoid duplicate email invites" % path)
        except requests.exceptions.ConnectionError as e:
            self.logger.error("Could not reach UMC server: %r" % e)

    def run(self):
        self.logger.info("Starting the filesystem watch to trigger invitation emails via the UMC")
        while True:
            self.logger.debug("Checking queue directory for new files: %s", self.queue_directory)
            for filename in self.queue_directory.glob("*.send"):
                self.handle_file(filename)

            time.sleep(5)


if __name__ == "__main__":
    invitation = Invitation()
    invitation.run()
