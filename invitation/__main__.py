# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import asyncio
import logging
import sys
from importlib.metadata import version
from typing import Awaitable, Callable

from univention.provisioning.consumer import MessageHandler, ProvisioningConsumerClient
from univention.provisioning.models import Message

from .config import Loglevel, get_selfservice_consumer_settings
from .consumer import SelfServiceConsumer

LOG_FORMAT = "%(asctime)s %(levelname)-5s [%(module)s.%(funcName)s:%(lineno)d] %(message)s"

logger = logging.getLogger(__name__)


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


def main() -> None:
    _settings = get_selfservice_consumer_settings()
    configure_logging(_settings.log_level)
    invitation = SelfServiceConsumer()
    asyncio.run(start_consumer(ProvisioningConsumerClient, MessageHandler, invitation.handle_user_event))


if __name__ == "__main__":
    main()
