# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import json

from univention.testing.helm.auth_flavors.password_usage import AuthPasswordUsageViaEnv
from univention.testing.helm.auth_flavors.secret_generation import AuthSecretGenerationOwner
from univention.testing.helm.auth_flavors.username import AuthUsername

# class TestAuth(SecretViaEnv, AuthPasswordOwner, Auth):
#     config_map_name = "release-name-selfservice-consumer-common"
#     secret_name = "release-name-selfservice-consumer-provisioning-api"

#     default_username = "selfservice"
#     derived_password = "827fe91a427f833a5f1895003679545d49d4d81d"


# class TestAuthRegistration(AuthPasswordSecret):
#     """Verify that the password value is correctly embedded within the key "registration"."""

#     secret_name = "release-name-selfservice-consumer-provisioning-api"
#     path_password = "stringData.registration"

#     is_secret_owner = True

#     def get_password(self, result):
#         secret = result.get_resource(kind="Secret", name=self.secret_name)
#         registration_json = secret.findone(self.path_password)
#         registration = json.loads(registration_json)
#         return registration["password"]


class SettingsTestProvisioningApiSecret:
    secret_name = "release-name-selfservice-consumer-provisioning-api"
    prefix_mapping = {"provisioningApi.auth": "auth"}

    # for AuthPasswordUsageViaEnv
    sub_path_env_password = "env[?@name=='PROVISIONING_API_PASSWORD']"
    workload_name = "release-name-selfservice-consumer"


class TestChartCreatesProvisioningApiSecretAsOwner(SettingsTestProvisioningApiSecret, AuthSecretGenerationOwner):
    derived_password = "827fe91a427f833a5f1895003679545d49d4d81d"


class TestSelfServiceConsumerUsesProvisioningApiCredentialsByEnv(
    SettingsTestProvisioningApiSecret, AuthPasswordUsageViaEnv
):
    pass


class TestSelfServiceConsumerInitContainerUsesProvisioningApiCredentialsByEnv_WaitForProvisioningApi(
    SettingsTestProvisioningApiSecret, AuthPasswordUsageViaEnv
):
    container_name = "wait-for-provisioning-api"


class TestAuthRegistrationUsername(SettingsTestProvisioningApiSecret, AuthUsername):
    """Verify that the username is correctly embedded within the key "registration"."""

    path_username = "stringData.registration"
    default_username = "selfservice"

    is_secret_owner = True

    def get_username(self, result):
        secret = result.get_resource(kind="Secret", name=self.secret_name)
        registration_json = secret.findone(self.path_username)
        registration = json.loads(registration_json)
        return registration["name"]
