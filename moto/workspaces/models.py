#
##
##
### NOTE: base code written by arvind.  editted by jbachell
##
##
#


import re
from datetime import datetime

from boto3 import Session

from moto.core import BaseBackend
from moto.core.utils import iso_8601_datetime_without_milliseconds
from moto.sts.models import ACCOUNT_ID
from uuid import uuid4
from .exceptions import (
    InvalidArn,
    InvalidName,
    WorkspaceDoesNotExist,
)

import random
import string


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


class Workspace:
    def __init__(self, workspace_id, directory_id, user_name, ip_address, state,
        bundle_id, subnet_id, computer_name, modification_states, workspaceProperties,
        rootEncEnabled, userEncEnabled, volumeKey):
        self.workspace_id = workspace_id
        self.directory_id = directory_id
        self.user_name = user_name
        self.ip_address = ip_address
        self.state = state
        self.bundle_id = bundle_id
        self.subnet_id = subnet_id
        self.computer_name = computer_name
        self.modification_states = modification_states

        if workspaceProperties:
            self.workspaceProperties = workspaceProperties
        else:
            self.workspaceProperties = {
                "RunningMode": "AUTO_STOP",
                "RunningModeAutoStopTimeoutInMinutes": 60,
                "RootVolumeSizeGib": 80,
                "UserVolumeSizeGib": 50,
                "ComputeTypeName": "STANDARD"
            }

        if volumeKey:
            self.volumeKey = volumeKey
            if userEncEnabled:
                self.userEncEnabled = userEncEnabled
            if rootEncEnabled:
                self.rootEncEnabled = rootEncEnabled

    def resp_workspace_invalid_state(self):
        return {'FailedRequests': [
                        {
                            "ErrorCode": "ResourceInvalidState.Workspace",
                            "WorkspaceId": "" + self.workspace_id,
                            "ErrorMessage": "The specified WorkSpace has an invalid state for this operation."
                        }
                    ],
                'ResponseMetadata': sample_responseMetaData
                }

    def stop(self):
        if self.state == "STOPPED":
            return self.resp_workspace_invalid_state()
        self.state = "STOPPED"
        return {'FailedRequests': []}

    def start(self):
        if self.state == "AVAILABLE":
            return self.resp_workspace_invalid_state()
        self.state = "AVAILABLE"
        return {'FailedRequests': []}

    def reboot(self):
        if self.state == "REBOOTING":
            return self.resp_workspace_invalid_state()
        self.state = "REBOOTING"
        return {'FailedRequests': []}

    # def rebuild(self):
    #     self.state = ""


class WorkspaceBackend(BaseBackend):
    accepted_role_arn_format = re.compile(
        "arn:aws:iam::(?P<account_id>[0-9]{12}):role/.+"
    )

    def __init__(self, region_name):
        self.workspaces = []
        self.region_name = region_name
        self._account_id = None

    def resp_workspace_does_not_exist(self, id):
        return {'FailedRequests': [
                {
                    "ErrorCode": "ResourceNotFound.Workspace",
                    "WorkspaceId": "" + id,
                    "ErrorMessage": "The specified WorkSpace could not be found."
                }
            ],
            'ResponseMetadata': sample_responseMetaData
        }

    def create_workspaces(self, directory_id, bundle_id, user_name, tags,
        workspaceProperties, rootEncEnabled, userEncEnabled, volumeKey):
        # self._validate_name(name)
        # self._validate_role_arn(roleArn)
        # try:
        #     return self.describe_state_machine(arn)
        # except WorkspaceDoesNotExist:

        lettersAndDigits = string.ascii_letters + string.digits
        workspace_id = 'ws-'+ ''.join((random.choice(lettersAndDigits) for i in range(10)))
        ip_address = '0.0.0.0'
        state = 'STOPPED'
        #state = 'AVAILABLE'
        subnet_id = 'subnet-000000000000000abc'
        computer_name = 'A-0000000000ABC'
        modification_states = []

        workspace = Workspace(workspace_id, directory_id, user_name, ip_address, state, bundle_id,
            subnet_id, computer_name, modification_states, workspaceProperties, rootEncEnabled,
            userEncEnabled, volumeKey)
        self.workspaces.append(workspace)

        return workspace

    def describe_workspaces(self, workspaceIds, directoryId, userName,
        bundleId, limit, nextToken):
        ret = sorted(
            [
                {
                    "WorkspaceId": ws.workspace_id,
                    "DirectoryId": ws.directory_id,
                    "UserName": ws.user_name,
                    "IpAddress": ws.ip_address,
                    "State": ws.state,
                    "BundleId": ws.bundle_id,
                    "SubnetId": ws.subnet_id,
                    "ComputerName": ws.computer_name,
                    "WorkspaceProperties": ws.workspaceProperties,
                    "ModificationStates": ws.modification_states
                }
                for ws in self.workspaces
            ],
            key=lambda x: x["UserName"],
        )

        if workspaceIds:
            temp = []
            for id in workspaceIds:
                temp += list(filter(lambda x: x.workspace_id == id, ret))
            ret = temp
        if directoryId:
            temp = []
            for id in directoryId:
                temp += list(filter(lambda x: x.directory_id == id, ret))
            ret = temp
        if userName:
            temp = []
            for id in userName:
                temp += list(filter(lambda x: x.user_name == id, ret))
            ret = temp
        if bundleId:
            temp = []
            for id in userName:
                temp += list(filter(lambda x: x.bundle_id == id, ret))
            ret = temp
        #exception for limit being less than zero should already
        #be caught in boto3
        if limit > 0:
            ret = ret[:limit]

        if nextToken:
            lettersAndDigits = string.ascii_letters[:6] + string.digits
            ret['NextToken'] = ''.join((random.choice(lettersAndDigits) for i in range(8))) + '-' \
                + ''.join((random.choice(lettersAndDigits) for i in range(4))) + '-' \
                + ''.join((random.choice(lettersAndDigits) for i in range(4))) + '-' \
                + ''.join((random.choice(lettersAndDigits) for i in range(4))) + '-' \
                + ''.join((random.choice(lettersAndDigits) for i in range(12))) + '-'

        return ret

    def stop_workspaces(self, id):
        #FIXME: can be more efficient??
        workspace = list(filter(lambda x: x.workspace_id == id, self.workspaces))
        if not workspace:
            return self.resp_workspace_does_not_exist(id)
        # if len(workspace) > 1:
        #     #two workspaces cannot have the same id?
        #     response = {'FailedRequests': [
        #             {
        #                 "ErrorCode": "Workspace",
        #                 "WorkspaceId": "" + self.workspace_id,
        #                 "ErrorMessage": "The specified WorkSpace has the same id."
        #             }
        #         ]
        #     }
        #     return response
        return workspace[0].stop()


    def start_workspaces(self, id):
        #FIXME: can be more efficient??
        workspace = list(filter(lambda x: x.workspace_id == id, self.workspaces))
        if not workspace:
            return self.resp_workspace_does_not_exist(id)
        # if len(workspace) > 1:
        #     #two workspaces cannot have the same id?
        #     response = {'FailedRequests': [
        #             {
        #                 "ErrorCode": "Workspace",
        #                 "WorkspaceId": "" + self.workspace_id,
        #                 "ErrorMessage": "The specified WorkSpace has the same id."
        #             }
        #         ]
        #     }
        #     return response
        return workspace[0].start()

    def reboot_workspaces(self, id):
        #FIXME: can be more efficient??
        workspace = list(filter(lambda x: x.workspace_id == id, self.workspaces))
        if not workspace:
            return self.resp_workspace_does_not_exist(id)
        # if len(workspace) > 1:
        #     #two workspaces cannot have the same id?
        #     response = {'FailedRequests': [
        #             {
        #                 "ErrorCode": "Workspace",
        #                 "WorkspaceId": "" + self.workspace_id,
        #                 "ErrorMessage": "The specified WorkSpace has the same id."
        #             }
        #         ]
        #     }
        #     return response
        return workspace[0].reboot()

    def rebuild_workspaces(self, id):
        #FIXME: can be more efficient??
        workspace = list(filter(lambda x: x.workspace_id == id, self.workspaces))
        if not workspace:
            return self.resp_workspace_does_not_exist(id)
        # if len(workspace) > 1:
        #     #two workspaces cannot have the same id?
        #     response = {'FailedRequests': [
        #             {
        #                 "ErrorCode": "Workspace",
        #                 "WorkspaceId": "" + self.workspace_id,
        #                 "ErrorMessage": "The specified WorkSpace has the same id."
        #             }
        #         ]
        #     }
        #     return response
        try:
            self.workspaces.remove(workspace[0])
            return {'FailedRequests': []}
        except:
            return {'FailedRequests': ["should not be here"]}

    def reset(self):
        region_name = self.region_name
        self.__dict__ = {}
        self.__init__(region_name)


workspace_backends = {}
for region in Session().get_available_regions("workspaces"):
    workspace_backends[region] = WorkspaceBackend(region)
for region in Session().get_available_regions(
    "workspaces", partition_name="aws-us-gov"
):
    workspace_backends[region] = WorkspaceBackend(region)
for region in Session().get_available_regions("workspaces", partition_name="aws-cn"):
    workspace_backends[region] = WorkspaceBackend(region)
