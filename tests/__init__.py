# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import os

ENV_DEFAULTS = {
    "UMC_SERVER_URL": "http://umc-server",
    "UMC_ADMIN_USER": "admin",
    "UMC_ADMIN_PASSWORD": "adminpassword",
    "PROVISIONING_API_USERNAME": "self-service",
    "PROVISIONING_API_PASSWORD": "selfservicepassword",
    "PROVISIONING_API_BASE_URL": "localhost",
}


def set_test_env_vars():
    for var, default in ENV_DEFAULTS.items():
        if var.lower() in (key.lower() for key in os.environ):
            continue
        os.environ[var] = default
        print(f"{var} was not explicitly set, setting the following default: {default}")
