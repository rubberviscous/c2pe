# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This example creates an OAuth 2.0 refresh token for the Google Ads API.

This illustrates how to step through the OAuth 2.0 native / installed
application flow.

It is intended to be run from the command line and requires user input.
"""

from __future__ import absolute_import

import argparse
import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..", "..", "..", ".."))
sys.path.append(path)

from google_auth_oauthlib.flow import InstalledAppFlow
from c2pe.backends.google.authentication.utils import save_token


SCOPE = u'https://www.googleapis.com/auth/documents'


def main(client_secrets_path, scopes, token_path):
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_path, scopes=scopes)

    credentials = flow.run_console()
    save_token(credentials, token_path)

    print('Access token: %s' % flow.credentials.token)
    print('Refresh token: %s' % flow.credentials.refresh_token)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generates OAuth 2.0 credentials with the specified '
                    'client secrets file.')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('--client_secrets_path', required=True,
                        help=('Path to the client secrets JSON file from the '
                              'Google Developers Console that contains your '
                              'client ID and client secret.'))
    parser.add_argument('--additional_scopes', default=None,
                        help=('Additional scopes to apply when generating the '
                              'refresh token. Each scope should be separated '
                              'by a comma.'))
    parser.add_argument('--token_path', required=True,
                        help=('Where to save the token'))
    args = parser.parse_args()

    configured_scopes = [SCOPE]

    if args.additional_scopes:
        configured_scopes.extend(args.additional_scopes.replace(' ', '')
                                 .split(','))

    main(args.client_secrets_path, configured_scopes, args.token_path)
# credentials = flow.run_console()
#
# token_path = os.environ.get('GOOGLE_TOKEN_PATH')
# save_token(credentials, token_path)