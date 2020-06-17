from __future__ import unicode_literals

import json

from moto.core.responses import BaseResponse
from moto.core.utils import amzn_request_id
from .exceptions import AWSError
from .models import workspace_backends

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


class WorkspaceResponse(BaseResponse):
    @property
    def workspace_backend(self):
        return workspace_backends[self.region]

    @amzn_request_id
    def create_workspaces(self):
        # FIXME: handle multi create
        workspaces = self._get_param("Workspaces")
        directory_id = workspaces[0]["DirectoryId"]
        user_name = workspaces[0]["UserName"]
        bundle_id = workspaces[0]["BundleId"]
        # tags = workspaces[0]["tags"]
        try:
            state_machine = self.workspace_backend.create_workspaces(
                directory_id=directory_id, bundle_id=bundle_id, user_name=user_name
            )
            response = {
                "FailedRequests": []
            }
            return 200, {}, json.dumps(response)
        except AWSError as err:
            return err.response()

    @amzn_request_id
    def describe_workspaces(self):
        # FIXME: handle filtering
        list_all = self.workspace_backend.describe_workspaces()

        response = {"Workspaces": list_all, "ResponseMetadata": sample_responseMetaData}
        return json.dumps(response)

    @amzn_request_id
    def stop_workspaces(self):
        # FIXME: handle multi stop
        reqs = self._get_param("StopWorkspaceRequests")
        workspace_id = reqs[0]["WorkspaceId"]

        response = self.workspace_backend.stop_workspaces(workspace_id)
        # response = {"FailedRequests": []}

        # FIXME: is this right?
        #return 200, {}, json.dumps(response)
        return json.dumps(response)

    @amzn_request_id
    def start_workspaces(self):
        # FIXME: handle multi stop
        reqs = self._get_param("StartWorkspaceRequests")
        workspace_id = reqs[0]["WorkspaceId"]

        response = self.workspace_backend.start_workspaces(workspace_id)
        # response = {"FailedRequests": []}

        # FIXME: is this right?
        #return 200, {}, json.dumps(response)
        return json.dumps(response)

    @amzn_request_id
    def reboot_workspaces(self):
        # FIXME: handle multi stop
        reqs = self._get_param("RebootWorkspaceRequests")
        workspace_id = reqs[0]["WorkspaceId"]

        response = self.workspace_backend.start_workspaces(workspace_id)
        # response = {"FailedRequests": []}

        # FIXME: is this right?
        #return 200, {}, json.dumps(response)
        return json.dumps(response)

    @amzn_request_id
    def start_workspaces(self):
        pass
        # # FIXME: handle multi stop
        # reqs = self._get_param("StopWorkspaceRequests")
        # workspace_id = reqs[0]["WorkspaceId"]
        #
        # response = self.workspace_backend.start_workspaces(workspace_id)
        # # response = {"FailedRequests": []}
        #
        # # FIXME: is this right?
        # #return 200, {}, json.dumps(response)
        # return json.dumps(response)
