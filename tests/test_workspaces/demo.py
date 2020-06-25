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

def test_real():
    client = boto3.client('workspaces')

    lst = client.describe_workspaces()

    print(lst)



@mock_workspaces
def test_mock():
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


test_real()
test_mock()
