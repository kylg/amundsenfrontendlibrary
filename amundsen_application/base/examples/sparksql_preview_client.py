import logging
import requests
import uuid
from flask import Response as FlaskResponse, make_response, jsonify
from http import HTTPStatus
from requests import Response
from typing import Dict
from amundsen_application.base.base_preview_client import BasePreviewClient
from requests import Response
from typing import Any, Dict  # noqa: F401
from amundsen_application.models.preview_data import ColumnItem, PreviewData, PreviewDataSchema

# 'main' is an existing default Superset database which serves for demo purposes
DEFAULT_DATABASE_MAP = {
    'main': 1,
}
DEFAULT_URL = 'http://localhost:8088/superset/sql_json/'


class SparksqlPreviewClient(BasePreviewClient):
    def __init__(self,
                 *,
                 database_map: Dict[str, int] = DEFAULT_DATABASE_MAP,
                 url: str = DEFAULT_URL) -> None:
        self.database_map = database_map
        self.headers = {}
        self.url = url

    def get_preview_data(self, params: Dict, optionalHeaders: Dict = None) -> FlaskResponse:
        """
        Returns a FlaskResponse object, where the response data represents a json object
        with the preview data accessible on 'preview_data' key. The preview data should
        match amundsen_application.models.preview_data.PreviewDataSchema
        """
        try:
            # Clone headers so that it does not mutate instance's state
            headers = dict(self.headers)

            # Merge optionalHeaders into headers
            if optionalHeaders is not None:
                headers.update(optionalHeaders)

            # Request preview data
            #response = self.post_to_sql_json(params=params, headers=headers)

            # Verify and return the results
            #response_dict = response.json()

            columns = [ColumnItem('sales', 'Int'), ColumnItem('time_id', 'String'), ColumnItem('product_id', 'String'), ColumnItem('customer_id', 'String')]
            #rows = response_dict['data']
            rows = [{'sales':30, 'time_id':'2020-05-30', 'product_id':'afa-0102', 'customer_id':'df01'}]
            preview_data = PreviewData(columns, rows)
            data = PreviewDataSchema().dump(preview_data)[0]
            errors = PreviewDataSchema().load(data)[1]
            if not errors:
                payload = jsonify({'preview_data': data})
                return make_response(payload, HTTPStatus.OK)
            else:
                return make_response(jsonify({'preview_data': {}}), HTTPStatus.INTERNAL_SERVER_ERROR)
        except Exception as e:
            return make_response(jsonify({'preview_data': {}}), HTTPStatus.INTERNAL_SERVER_ERROR)
