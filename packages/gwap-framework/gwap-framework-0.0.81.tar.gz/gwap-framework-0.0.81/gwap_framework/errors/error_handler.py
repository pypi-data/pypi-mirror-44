import json
from typing import Union, Tuple, List

from flask import Blueprint
from schematics.exceptions import DataError
from sqlalchemy.exc import IntegrityError

from gwap_framework.app import GwapApp
from gwap_framework.errors.base import BaseError


def default_error_handler(error: Exception):
    """Returns Internal server error"""
    return json.dumps({'message': str(error), 'code': getattr(error, 'code', 500), 'status': 'internal_server_error'}), {'Content-Type': 'application/json'}


def error_handler(error: BaseError):
    """Returns Internal server error"""
    return json.dumps(error.to_dict()), getattr(error, 'code'), {'Content-Type': 'application/json'}


def data_error_handler(error: DataError):
    """Returns Internal server error"""
    return json.dumps({
            'code': 422,
            'message': error.to_primitive(),
            'status': 'invalid_payload'
        }), 422, {'Content-Type': 'application/json'}


def integrity_error_handler(error: IntegrityError):
    """Returns Internal server error"""
    return json.dumps({
            'code': 500,
            'message': str(error.orig),
            'status': 'integrity_error'
        }), 500, {'Content-Type': 'application/json'}


class GwapErrorHandlerConfig:
    """
        GwapExceptionHandlerConfig is a middleware which register the errors handlers.
    """
    app = None

    def __init__(self, app: Union[GwapApp, Blueprint], handlers: List[Tuple] = []):
        if app:
            self.init_app(app, handlers)

    def init_app(self, app: GwapApp, handlers: List[Tuple]) -> None:
        self.app = app
        self.app.register_error_handler(Exception, default_error_handler)
        self.app.register_error_handler(BaseError, error_handler)
        self.app.register_error_handler(DataError, data_error_handler)
        self.app.register_error_handler(IntegrityError, integrity_error_handler)
        for error, handler in handlers:
            self.app.register_error_handler(error, handler)
