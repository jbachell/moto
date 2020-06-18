from __future__ import unicode_literals

import boto3
import sure  # noqa
import datetime

from datetime import datetime
from botocore.exceptions import ClientError
from nose.tools import assert_raises

from moto import mock_sts, mock_workspaces
from moto.core import ACCOUNT_ID

region = "us-east-1"
simple_definition = (
    '{"Comment": "An example of the Amazon States Language using a choice state.",'
    '"StartAt": "DefaultState",'
    '"States": '
    '{"DefaultState": {"Type": "Fail","Error": "DefaultStateError","Cause": "No Matches!"}}}'
)
account_id = None

#helper functions!

def does_nesting_work():
    client = boto3.client('workspaces', aws_access_key_id='id3',
                              aws_secret_access_key='secret3',
                              aws_session_token='token3')

    workspace = client.create_workspaces(
                        Workspaces=[{
                            'DirectoryId': "d-29381asfdw",
                            'BundleId': "wsb-asd42hfg1",
                            'UserName': "janedoe3"
                        }]
                    )

    workspace = client.create_workspaces(
                        Workspaces=[{
                            'DirectoryId': "d-29381asfdw",
                            'BundleId': "wsb-asd42hfg1",
                            'UserName': "janedoe4"
                        }]
                    )

def does_nesting_work_with_client(client):
    # client = boto3.client('workspaces', aws_access_key_id='id3',
    #                           aws_secret_access_key='secret3',
    #                           aws_session_token='token3')

    workspace = client.create_workspaces(
                        Workspaces=[{
                            'DirectoryId': "d-29381asfdw",
                            'BundleId': "wsb-asd42hfg1",
                            'UserName': "janedoe5"
                        }]
                    )

    workspace = client.create_workspaces(
                        Workspaces=[{
                            'DirectoryId': "d-29381asfdw",
                            'BundleId': "wsb-asd42hfg1",
                            'UserName': "janedoe6"
                        }]
                    )



@mock_workspaces
def test_describe_workspaces_returns_empty_list_by_default():
    client = boto3.client("workspaces", region_name=region)
    #
    list = client.describe_workspaces()
    list["Workspaces"].should.be.empty

#describe_workspaces()

@mock_workspaces
# @mock_sts
def test_describe_workspaces_returns_created_workspaces():
    # client = boto3.client("workspaces", region_name=region)
    #
    # workspace2 = client.create_workspaces(
    #     Workspaces=[{
    #         'DirectoryId': "d-29381asfdw",
    #         'BundleId': "wsb-asd42hfg1",
    #         'UserName': "johndoe"
    #     }]
    # )
    # workspace1 = client.create_workspaces(
    #     Workspaces=[{
    #         'DirectoryId': "d-29381asfdw",
    #         'BundleId': "wsb-asd42hfg1",
    #         'UserName': "janedoe"
    #     }]
    # )
    # lst = client.describe_workspaces()
    #
    # lst["ResponseMetadata"]["HTTPStatusCode"].should.equal(200)
    # lst["Workspaces"].should.have.length_of(2)
    # lst["Workspaces"][0]["UserName"].should.equal("janedoe")
    # lst["Workspaces"][1]["UserName"].should.equal("johndoe")
    # print("here")
    # print(list(lst['Workspaces']))

    #client = boto3.client("workspaces", region_name=region)
    #lst = client.describe_workspaces()
    #print("jere")
    #print(list(lst['Workspaces']))
    #print("here")
    client = boto3.client('workspaces', aws_access_key_id='id1',
                              aws_secret_access_key='secret1',
                              aws_session_token='token1')
    #print("here")
    temp = client.create_workspaces(
                        Workspaces=[{
                            'DirectoryId': "d-29381asfdw",
                            'BundleId': "wsb-asd42hfg1",
                            'UserName': "ajanedoe1"
                        }]
                    )
    #print("here")
    workspace = client.create_workspaces(
                        Workspaces=[{
                            'DirectoryId': "d-29381asfdw",
                            'BundleId': "wsb-asd42hfg1",
                            'UserName': "ajanedoe2"
                        }]
                    )
    lst = client.describe_workspaces()
    print("here")
    #print(list(lst['Workspaces']))
    lst["Workspaces"].should.have.length_of(2)

    client = boto3.client('workspaces', aws_access_key_id='id2',
                              aws_secret_access_key='secret2',
                              aws_session_token='token2')

    workspace = client.create_workspaces(
                        Workspaces=[{
                            'DirectoryId': "d-29381asfdw",
                            'BundleId': "wsb-asd42hfg1",
                            'UserName': "janedoe1"
                        }]
                    )

    workspace = client.create_workspaces(
                        Workspaces=[{
                            'DirectoryId': "d-29381asfdw",
                            'BundleId': "wsb-asd42hfg1",
                            'UserName': "janedoe2"
                        }]
                    )
    lst = client.describe_workspaces()
    #print("here")
    #print(list(lst['Workspaces']))
    print(len(list(lst['Workspaces'])))
    lst["Workspaces"].should.have.length_of(4)

    does_nesting_work()
    lst = client.describe_workspaces()
    print(len(list(lst['Workspaces'])))
    lst["Workspaces"].should.have.length_of(6)

    does_nesting_work_with_client(client)
    lst = client.describe_workspaces()
    print(len(list(lst['Workspaces'])))
    lst["Workspaces"].should.have.length_of(8)

    print(temp)

    client.start_workspaces( StartWorkspaceRequests=[
                                {
                                    'WorkspaceId': temp['WorkspaceId']
                                },
                            ])
    lst = client.describe_workspaces()
    print(list(lst)[0])

def _get_account_id():
    global account_id
    if account_id:
        return account_id
    sts = boto3.client("sts", region_name=region)
    identity = sts.get_caller_identity()
    account_id = identity["Account"]
    return account_id


def _get_default_role():
    return "arn:aws:iam::" + _get_account_id() + ":role/unknown_sf_role"


test_describe_workspaces_returns_empty_list_by_default()
test_describe_workspaces_returns_created_workspaces()
