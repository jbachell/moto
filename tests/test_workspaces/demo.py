#
##
##
### NOTE: base code written by arvind.  editted by jbachell
##
##
#


from __future__ import unicode_literals

import boto3
import datetime
import json

from datetime import datetime
from botocore.exceptions import ClientError

from moto import mock_sts, mock_workspaces
from moto.core import ACCOUNT_ID


#
#
### starting demo here!
#
#



def test_boto3_workspaces():
    client = boto3.client('workspaces')

    temp = client.create_workspaces(
                        Workspaces=[{
                            'DirectoryId': "d-29381asfdw",
                            'BundleId': "wsb-asd42hfg1",
                            'UserName': "ajanedoe1"
                        }]
                    )

    lst = client.describe_workspaces()

    print(lst)

@mock_workspaces
wrapper_func():
    print("Calling boto3.workspaces!")

    test_boto3_workspaces()

wrapper_fun()
