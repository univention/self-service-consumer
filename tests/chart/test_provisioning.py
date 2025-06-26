# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import json

from univention.testing.helm.client.provisioning_api import (
    Auth,
    AuthPasswordOwner,
    AuthPasswordSecret,
    AuthUsername,
    Connection,
    SecretViaEnv,
)


class TestAuth(SecretViaEnv, AuthPasswordOwner, Auth):
    config_map_name = "release-name-selfservice-consumer-common"
    secret_name = "release-name-selfservice-consumer-provisioning-api"

    default_username = "selfservice"
    derived_password = "46dc2d43d2cfb31b484b3ded24376b13be696924"


class TestAuthRegistration(AuthPasswordSecret):
    """Verify that the password value is correctly embedded within the key "registration"."""

    secret_name = "release-name-selfservice-consumer-provisioning-api"
    path_password = "stringData.registration"

    is_secret_owner = True

    def get_password(self, result):
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        registration_json = secret.findone(self.path_password)
        registration = json.loads(registration_json)
        return registration["password"]


class TestAuthRegistrationUsername(AuthUsername):
    """Verify that the username is correctly embedded within the key "registration"."""

    secret_name = "release-name-selfservice-consumer-provisioning-api"
    path_username = "stringData.registration"
    default_username = "selfservice"

    is_secret_owner = True

    def get_username(self, result):
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        registration_json = secret.findone(self.path_username)
        registration = json.loads(registration_json)
        return registration["name"]


class TestConnection(Connection):
    config_map_name = "release-name-selfservice-consumer-common"

    path_provisioning_api_url = "data.PROVISIONING_API_BASE_URL"
