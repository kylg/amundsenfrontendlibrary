import logging
import requests
from flask import Response as FlaskResponse, make_response, jsonify
from http import HTTPStatus
from amundsen_application.base.base_preview_client import BasePreviewClient
from typing import Any, Dict  # noqa: F401
from amundsen_application.models.preview_data import ColumnItem, PreviewData, PreviewDataSchema
import os

DEFAULT_URL = 'http://localhost:5003/preview_data'


class SparksqlPreviewClient(BasePreviewClient):

    def __init__(self) -> None:
        super().__init__()
        self.url = os.environ.get('PREVIEW_SERVICE_ENDPOINT', DEFAULT_URL)
        logging.info("Using preview service at "+self.url)

    def get_preview_data(self, params: Dict, optionalHeaders: Dict = None) -> FlaskResponse:

        """
        Returns a FlaskResponse object, where the response data represents a json object
        with the preview data accessible on 'preview_data' key. The preview data should
        match amundsen_application.models.preview_data.PreviewDataSchema
        :param  {"database":"","schema":"","tableName":""}
        """
        logging.info('get preview data of {}'
                 .format(params))
        try:
            with requests.Session() as s:
                response = s.post(self.url, json=params, timeout=10)
                status_code = response.status_code
                # the table has no preview data
                if status_code == HTTPStatus.NOT_FOUND:
                    return make_response(jsonify({'preview_data': {}}), HTTPStatus.OK)
                if status_code == HTTPStatus.OK:
                    preview_data = response.json()
                    data = PreviewDataSchema().dump(preview_data)[0]
                    payload = jsonify({'preview_data': data})
                    return make_response(payload, HTTPStatus.OK)
                else:
                    return make_response(jsonify({'preview_data': {}}), HTTPStatus.INTERNAL_SERVER_ERROR)
        except Exception as e:
            payload = jsonify({'description': None, 'msg': 'Encountered exception: ' + str(e)})
            return make_response(payload, HTTPStatus.INTERNAL_SERVER_ERROR)
