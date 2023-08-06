import os
import logging

import yaml

log = logging.getLogger()


def create(kube_filepath, account_no, eks):
    if not os.path.exists(kube_filepath):
        log.info('Creating kube config file at %s', kube_filepath)
        cluster_info = eks.describe_cluster(name=os.getenv('ClusterName'))
        certificate = cluster_info['cluster']['certificateAuthority']['data']
        endpoint = cluster_info['cluster']['endpoint']
        cluster_arn = 'arn:aws:eks:' + os.getenv('AWS_REGION') + ':' + account_no + ':cluster/' + os.getenv('ClusterName')

        kube_content = {}
        kube_content['apiVersion'] = 'v1'
        kube_content['clusters'] = [
            {
                'cluster':
                    {
                        'server': endpoint,
                        'certificate-authority-data': certificate
                    },
                'name': cluster_arn
            }
        ]

        kube_content['contexts'] = [
            {
                'context':
                    {
                        'cluster': cluster_arn,
                        'user': cluster_arn
                    },
                'name': cluster_arn
            }
        ]

        kube_content['current-context'] = cluster_arn
        kube_content['kind'] = 'Config'
        kube_content['preferences'] = {}
        kube_content['users'] = [
            {
                'name': cluster_arn,
                'user': {
                            'exec': {
                                'apiVersion': 'client.authentication.k8s.io/v1alpha1',
                                'args': ['token', '-i', os.getenv('ClusterName'), '-r', os.getenv('IAMRole')],
                                'command': 'aws-iam-authenticator'
                            }
                    }
            }
        ]

        with open(kube_filepath, 'w') as outfile:
            yaml.safe_dump(kube_content, outfile, default_flow_style=False)
    else:
        log.info('kube config exist at %s', kube_filepath)
