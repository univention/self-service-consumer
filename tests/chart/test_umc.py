# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from univention.testing.helm.client.umc import Connection


class TestConnection(Connection):

    config_map_name = "release-name-selfservice-consumer-common"
