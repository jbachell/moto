#
##
##
### NOTE: base code written by arvind.  editted by jbachell
##
##
#


from __future__ import unicode_literals

import json

from moto.core.responses import BaseResponse
from moto.core.utils import amzn_request_id
from .exceptions import AWSError
from .models import workspace_backends
from .exceptions import (ClientError)

sample_responseMetaData =  {
    "ResponseMetadata": {
        "RequestId": "7d5dedc0-d7ed-4ab8-959c-e5138023aecb",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "7d5dedc0-d7ed-4ab8-959c-e5138023aecb",
            "content-type": "application/x-amz-json-1.1",
            "content-length": "12751",
            "date": "Mon, 08 Jun 2020 19:28:45 GMT"
        },
        "RetryAttempts": 0
    }
}

errValidation = "An error occurred (ValidationException) when calling the StopWorkspaces operation: The request is invalid."

class WorkspaceResponse(BaseResponse):
    @property
    def workspace_backend(self):
        return workspace_backends[self.region]

    @amzn_request_id
    def create_workspaces(self):
        result = {'FailedRequests': []}
        workspaces = self._get_param("Workspaces")
        for i in workspaces:
            directory_id = i["DirectoryId"]
            user_name = i["UserName"]
            bundle_id = i["BundleId"]
            # tags = workspaces[0]["tags"]
            try:
                state_machine = self.workspace_backend.create_workspaces(
                    directory_id=directory_id, bundle_id=bundle_id, user_name=user_name
                )
                response = {
                    "FailedRequests": []
                }
                #FIXME: right return here?
                return 200, {}, json.dumps(response)
            except AWSError as err:
                return err.response()

    @amzn_request_id
    def describe_workspaces(self, WorkspaceIds=[], DirectoryId='', UserName='',
        BundleId='', Limit=-1, NextToken=''):

        list_all = self.workspace_backend.describe_workspaces(WorkspaceIds, DirectoryId, UserName,
            BundleId, Limit, NextToken)

        response = {"Workspaces": list_all, "ResponseMetadata": sample_responseMetaData}
        return json.dumps(response)

    @amzn_request_id
    def stop_workspaces(self):
        result = {'FailedRequests': []}
        reqs = self._get_param("StopWorkspaceRequests")
        if len(reqs) > 25:
            raise ClientError(errValidation)
        for i in reqs:
            workspace_id = i["WorkspaceId"]
            response = self.workspace_backend.stop_workspaces(workspace_id)
            result['FailedRequests'] = result['FailedRequests'] + (response['FailedRequests'])
            #result.setdefault('FailedRequests', []).append(response['FailedRequests'])
        # response = {"FailedRequests": []}

        # FIXME: is this right?
        return 200, {}, json.dumps(result)
        #return json.dumps(response)

    @amzn_request_id
    def start_workspaces(self):
        result = {'FailedRequests': []}
        reqs = self._get_param("StartWorkspaceRequests")
        if len(reqs) > 25:
            raise ClientError(errValidation)
        for i in reqs:
            workspace_id = i["WorkspaceId"]
            response = self.workspace_backend.start_workspaces(workspace_id)
            result['FailedRequests'] = result['FailedRequests'] + (response['FailedRequests'])
            #result.setdefault('FailedRequests', []).append(response['FailedRequests'])
        # response = {"FailedRequests": []}

        # FIXME: is this right?
        return 200, {}, json.dumps(result)
        #return json.dumps(response)

    @amzn_request_id
    def reboot_workspaces(self):
        result = {'FailedRequests': []}
        reqs = self._get_param("RebootWorkspaceRequests")
        if len(reqs) > 25:
            raise ClientError(errValidation)
        for i in reqs:
            workspace_id = i["WorkspaceId"]
            response = self.workspace_backend.reboot_workspaces(workspace_id)
            result['FailedRequests'] = result['FailedRequests'] + (response['FailedRequests'])
            #result.setdefault('FailedRequests', []).append(response['FailedRequests'])
        # response = {"FailedRequests": []}

        # FIXME: is this right?
        return 200, {}, json.dumps(result)
        #return json.dumps(response)

    @amzn_request_id
    def rebuild_workspaces(self):
        result = {'FailedRequests': []}
        reqs = self._get_param("RebuildWorkspaceRequests")
        if len(reqs) > 25:
            raise ClientError(errValidation)
        for i in reqs:
            workspace_id = i["WorkspaceId"]
            response = self.workspace_backend.rebuild_workspaces(workspace_id)
            result['FailedRequests'] = result['FailedRequests'] + (response['FailedRequests'])
            #result.setdefault('FailedRequests', []).append(response['FailedRequests'])
        # response = {"FailedRequests": []}

        # FIXME: is this right?
        return 200, {}, json.dumps(result)
        #return json.dumps(response)
