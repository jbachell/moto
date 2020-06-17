from __future__ import unicode_literals
from moto.core.exceptions import RESTError


class SESSClientError(RESTError):
    code = 400


class SESSValidationError(SESSClientError):
    def __init__(self, *args, **kwargs):
        super(SESSValidationError, self).__init__("ValidationError", *args, **kwargs)
