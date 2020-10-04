# Copyright Contributors to the Amundsen project.
# SPDX-License-Identifier: Apache-2.0
import logging
import json
from http import HTTPStatus
from typing import Dict, Optional
from flask import Flask, Response, jsonify, make_response

from amundsen_application.config import LocalConfig
from amundsen_application.models.user import load_user, User
from amundsen_application.api.metadata.v0 import USER_ENDPOINT
from amundsen_application.api.utils.request_utils import request_metadata
from amundsen_application.api.v0 import current_user
from flaskoidc_azure import get_token_from_cache, get_user

LOGGER = logging.getLogger(__name__)

def get_access_headers(app: Flask) -> Optional[Dict]:
    """
    Function to retrieve and format the Authorization Headers
    that can be passed to various microservices who are expecting that.
    :param app: The instance of the current app.
    :return: A formatted dictionary containing access token
    as Authorization header.
    """
    try:
        access_token = get_token_from_cache(app.config['SCOPE'])
        return {'Authorization': 'Bearer {}'.format(access_token)}
    except Exception:
        return None


def get_auth_user(app: Flask) -> User:
    """
    Retrieves the user information from oidc token, and then makes
    a dictionary 'UserInfo' from the token information dictionary.
    We need to convert it to a class in order to use the information
    in the rest of the Amundsen application.
    :param app: The instance of the current app.
    :return: A class UserInfo (Note, there isn't a UserInfo class, so we use Any)
    """
    token = get_token_from_cache(app.config['SCOPE'])
    user_info = load_user(get_user(token))
    return user_info


def put_auth_user(app: Flask, user_info: Dict) -> Dict:
    """
    Add or update user into metadata service.
    :param user: user information
    :param app: The instance of the current app.
    :return: A class UserInfo (Note, there isn't a UserInfo class, so we use Any)
    """
    try:
        user = load_user(user_info)
        url = '{0}{1}/{2}'.format(app.config['METADATASERVICE_BASE'], USER_ENDPOINT, user.user_id)
        response = request_metadata(url=url, method='PUT', data=user.__dict__)
        status_code = response.status_code
        if status_code == HTTPStatus.OK:
            return response.json()
        else:
            return None
    except Exception as e:
        LOGGER.error("Exception encountered while putting user", e)
        return None


def get_logged_in_user(app: Flask) -> User:
    """
    Retrieves the user information from metadata service.
    :param app: The instance of the current app.
    :return: A class UserInfo (Note, there isn't a UserInfo class, so we use Any)
    """
    user = json.loads(current_user().data).get("user")
    user_info = load_user(user)
    return user_info


class OidcConfig(LocalConfig):
    AUTH_USER_METHOD = get_auth_user
    PUT_USER_METHOD = put_auth_user
    REQUEST_HEADERS_METHOD = get_access_headers
    LOGGED_IN_USER_METHOD = get_logged_in_user
