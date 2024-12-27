#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os

class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "370ddeb8-18bd-42c9-bab1-f34abc5e8be0")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "y528Q~sJ1Er-WNkDWsFzwnkPMp~9FmtpLb11~aZS")
