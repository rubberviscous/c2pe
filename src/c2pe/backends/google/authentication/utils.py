# """
# https://google-auth.readthedocs.io/en/latest/index.html
# """
import json
import os
import shutil

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

CREDENTIALS_INSTANCE_PARAMS = {
    'access_token': 'token',
    'refresh_token': 'refresh_token',
    'token_uri': 'token_uri',
    'client_id': 'client_id',
    'client_secret': 'client_secret',
    'scopes': 'scopes',
}


def get_credentials(token_path: str, refresh: bool = False) -> Credentials:
    """
    Returns a Credentials instance from the given token path

    Args:
        token_path: path to the token JSON
        refresh: whether to force-refresh the token; when false the token will be refreshed if expired

    Returns:
        Credentials instance
    """
    if not os.path.exists(token_path):
        raise FileNotFoundError()

    with open(token_path) as fh:
        data = json.load(fh)

    kwargs = {}
    for _in, _out in CREDENTIALS_INSTANCE_PARAMS.items():
        if _in == 'access_token':
            kwargs[_out] = None
        else:
            kwargs[_out] = data[_in]

    credentials = Credentials(**kwargs)

    if refresh or not credentials.valid:
        request = Request()
        credentials.refresh(request)

        save_token(credentials, token_path)

    return credentials


def save_token(credentials: Credentials, token_path: str):
    """
    Saves the token to the given path

    Args:
        credentials: a Credentials instance
        token_path: path to file on disk
    """
    data = {}
    for _out, _in in CREDENTIALS_INSTANCE_PARAMS.items():
        val = getattr(credentials, _in)

        data[_out] = val

    dirname, basename = os.path.split(token_path)
    tmp_path = os.path.join(dirname, f'.{basename}.tmp')

    with open(tmp_path, 'w') as fh:
        fh.write(json.dumps(data))

    shutil.move(tmp_path, token_path)
