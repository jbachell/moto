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
