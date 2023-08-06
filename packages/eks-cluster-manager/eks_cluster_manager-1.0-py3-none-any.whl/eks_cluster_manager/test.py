import os
import logging

import index

logging.basicConfig()
log = logging.getLogger()
log.setLevel('DEBUG')

os.environ['ClusterName'] = 'Cluster-SHwpOiXlS7pW'
os.environ['ClusterName'] = 'Cluster-5hUvXUEy82Ts'
os.environ['AWS_REGION'] = 'us-east-1'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
os.environ['IAMRole'] = 'arn:aws:iam::878756246442:role/cfn-ec2-lambda-admin-role'
context=None
x={
  "Records": [
    {
      "eventVersion": "2.1",
      "eventTime": "2019-03-18T14:45:40.091Z",
      "requestParameters": {
        "sourceIPAddress": "107.22.23.212"
      },
      "s3": {
        "configurationId": "4a5a4a50-9d95-456c-8215-facd02e5770e",
        "object": {
          "eTag": "a87c6213f46d203b0e936298d2c020b6",
          "sequencer": "005C8FAF140B66F611",
          "key": "aws-auth-cm.yaml",
          "size": 290
        },
        "bucket": {
          "arn": "arn:aws:s3:::avi-eks-yaml-1",
          "name": "kc-test789",
          "ownerIdentity": {
            "principalId": "A39FWI0FVGXB1"
          }
        },
        "s3SchemaVersion": "1.0"
      },
      "responseElements": {
        "x-amz-id-2": "l+5wyyHAjq/e6VlVQbsxcVkeBevhNrdIG3cGElJjS/derUpxTb03M40PvBe8iggmiRiOMGLxP4E=",
        "x-amz-request-id": "7457175A11A5DAAB"
      },
      "awsRegion": "us-east-1",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "AWS:AIDAICU5VCFUPAATBIFNK"
      },
      "eventSource": "aws:s3"
    }
  ]
}

index.handler(x, context)
