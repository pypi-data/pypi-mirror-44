import os
import uuid
import logging
import traceback

log = logging.getLogger()
log.setLevel('DEBUG')

import boto3
import yaml
from kubernetes import client, config

# https://medium.com/@alejandro.millan.frias/managing-kubernetes-from-aws-lambda-7922c3546249
import eks_cluster_manager.auth as auth
import eks_cluster_manager.kubeconfig as kubeconfig
import eks_cluster_manager.kubectl as kubectl

s3 = boto3.resource('s3')
cfn = boto3.client('cloudformation')


def run(event, context):
    log.info('Event %s', event)

    os.environ['PATH'] += os.pathsep + os.path.dirname(os.path.realpath(__file__))

    kube_filepath = '/tmp/kubeconfig'
    os.environ['KUBECONFIG'] = kube_filepath
    kubeconfig.create(kube_filepath, boto3.client('sts').get_caller_identity().get('Account'), boto3.client('eks'))

    eks = auth.EKSAuth(os.environ['ClusterName'], os.environ['AWS_REGION'])
    token = eks.get_token()
    log.info('EKS token %s', token)

    try:
        log.info('Loading kube config file %s', kube_filepath)
        config.load_kube_config(kube_filepath)
        log.info('Loaded kube config file %s', kube_filepath)
    except Exception as e:
        traceback.print_exc()

    configuration = client.Configuration()
    configuration.api_key['authorization'] = token
    configuration.api_key_prefix['authorization'] = 'Bearer'

    log.info('Instantiating kubernetes client')
    api = client.ApiClient(configuration)
    v1 = client.CoreV1Api(api)

    log.info('Invoke list_service_for_all_namespaces')
    ret = v1.list_service_for_all_namespaces()
    log.info('list_service_for_all_namespaces => %s', ret)

    s3Bucket = event['Records'][0]['s3']['bucket']['name']
    s3Key = event['Records'][0]['s3']['object']['key']
    confFile = '/tmp/' + s3Key
    s3.meta.client.download_file(s3Bucket, s3Key, confFile)

    with open(confFile, 'r') as f:
        kubectl.apply(yaml.load(f), api)

    existingParams = cfn.describe_stacks(StackName=os.environ['CFNStackName'])['Stacks'][0]['Parameters']
    log.info('Existing params %s', existingParams)
    cfn.update_stack(
        StackName=os.environ['CFNStackName'],
        UsePreviousTemplate=True,
        Capabilities=['CAPABILITY_NAMED_IAM'],
        Parameters=existingParams,
        Tags=[{'Key': 'UpdateMarker', 'Value': uuid.uuid4().hex}]
    )
    return 0
