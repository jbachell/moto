#
##
##
### NOTE: base code written by arvind.  editted by jbachell
##
##
#


from __future__ import unicode_literals
import json


class AWSError(Exception):
    TYPE = None
    STATUS = 400

    def __init__(self, message, type=None, status=None):
        self.message = message
        self.type = type if type is not None else self.TYPE
        self.status = status if status is not None else self.STATUS

    def response(self):
        return (
            json.dumps({"__type": self.type, "message": self.message}),
            dict(status=self.status),
        )

class InvalidArn(AWSError):
    TYPE = "InvalidArn"
    STATUS = 400


class InvalidName(AWSError):
    TYPE = "InvalidName"
    STATUS = 400


class WorkspaceDoesNotExist(AWSError):
    TYPE = "WorkspaceDoesNotExist"
    STATUS = 400

class ClientError(AWSError):
    TYPE = "ValidationError"
    STATUS = 400
