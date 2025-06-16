# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from univention.testing.helm.client.provisioning_api import Auth, Connection


class TestAuth(Auth):

    config_map_name = "release-name-selfservice-consumer-common"
    secret_name = "release-name-selfservice-consumer-provisioning-api"

    default_username = "selfservice"

    path_provisioning_api_url = "data.PROVISIONING_API_BASE_URL"


class TestConnection(Connection):

    config_map_name = "release-name-selfservice-consumer-common"

    path_provisioning_api_url = "data.PROVISIONING_API_BASE_URL"
