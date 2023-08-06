import re
import yaml
import logging

import kubernetes.client

log = logging.getLogger()


def apply(obj, client=None, **kwargs):
    ''' invoke the K8s API to create or replace a kubernetes object.
        The first attempt is to create(insert) this object; when this is rejected because
        of an existing object with same name, we attempt to patch this existing object.
        As a last resort, if even the patch is rejected, we *delete* the existing object
        and recreate from scratch.
        @param obj: complete object specification, including API version and metadata.
        @param client: (optional) preconfigured client environment to use for invocation
        @param kwargs: (optional) further arguments to pass to the create/replace call
        @return: response object from Kubernetes API call
    '''
    k8sApi = findK8sApi(obj, client)
    try:
        res = invokeApi(k8sApi, 'create', obj, **kwargs)
        log.info('K8s: %s created -> uid=%s', describe(obj), res.metadata.uid)
    except kubernetes.client.rest.ApiException as apiEx:
        log.info('Exception %s', apiEx.reason)
        try:
            # asking for forgiveness...
            res = invokeApi(k8sApi, 'patch', obj, **kwargs)
            log.info('K8s: %s PATCHED -> uid=%s', describe(obj), res.metadata.uid)
        except kubernetes.client.rest.ApiException as apiEx:
            if apiEx.reason != 'Unprocessable Entity': raise
            try:
                # second attempt... delete the existing object and re-insert
                log.info('K8s: replacing %s FAILED. Attempting deletion and recreation...', describe(obj))
                res = invokeApi(k8sApi, 'delete', obj, **kwargs)
                log.info('K8s: %s DELETED...', describe(obj))
                res = invokeApi(k8sApi, 'create', obj, **kwargs)
                log.info('K8s: %s CREATED -> uid=%s', describe(obj), res.metadata.uid)
            except Exception as ex:
                message = 'K8s: FAILURE updating %s. Exception: %s' % (describe(obj), ex)
                log.error(message)
                raise RuntimeError(message)
    return res


def patchObject(obj, client=None, **kwargs):
    k8sApi = findK8sApi(obj, client)
    try:
        res = invokeApi(k8sApi, 'patch', obj, **kwargs)
        log.info('K8s: %s PATCHED -> uid=%s', describe(obj), res.metadata.uid)
        return res
    except kubernetes.client.rest.ApiException as apiEx:
        if apiEx.reason == 'Unprocessable Entity':
            message = 'K8s: patch for %s rejected. Exception: %s' % (describe(obj), apiEx)
            log.error(message)
            raise RuntimeError(message)
        else:
            raise


def deleteObject(obj, client=None, **kwargs):
    k8sApi = findK8sApi(obj, client)
    try:
        res = invokeApi(k8sApi, 'delete', obj, **kwargs)
        log.info('K8s: %s DELETED. uid was: %s', describe(obj), res.details and res.details.uid or '?')
        return True
    except kubernetes.client.rest.ApiException as apiEx:
        if apiEx.reason == 'Not Found':
            log.warning('K8s: %s does not exist (anymore).', describe(obj))
            return False
        else:
            message = 'K8s: deleting %s FAILED. Exception: %s' % (describe(obj), apiEx)
            log.error(message)
            raise RuntimeError(message)



def findK8sApi(obj, client=None):
    ''' Investigate the object spec and lookup the corresponding API object
        @param client: (optional) preconfigured client environment to use for invocation
        @return: a client instance wired to the apriopriate API
    '''
    grp, _, ver = obj['apiVersion'].partition('/')
    if ver == '':
        ver = grp
        grp = 'core'
    # Strip 'k8s.io', camel-case-join dot separated parts. rbac.authorization.k8s.io -> RbacAuthorzation
    grp = ''.join(part.capitalize() for part in grp.rsplit('.k8s.io', 1)[0].split('.'))
    ver = ver.capitalize()

    k8sApi = '%s%sApi' % (grp, ver)
    return getattr(kubernetes.client, k8sApi)(client)


def invokeApi(k8sApi, action, obj, **args):
    ''' find a suitalbe function and perform the actual API invocation.
        @param k8sApi: client object for the invocation, wired to correct API version
        @param action: either 'create' (to inject a new objet) or 'replace','patch','delete'
        @param obj: the full object spec to be passed into the API invocation
        @param args: (optional) extraneous arguments to pass
        @return: response object from Kubernetes API call
    '''
    # transform ActionType from Yaml into action_type for swagger API
    kind = camel2snake(obj['kind'])
    # determine namespace to place the object in, supply default
    try: namespace = obj['metadata']['namespace']
    except: namespace = 'default'

    functionName = '%s_%s' %(action,kind)
    if hasattr(k8sApi, functionName):
        # namespace agnostic API
        function = getattr(k8sApi, functionName)
    else:
        functionName = '%s_namespaced_%s' %(action,kind)
        function = getattr(k8sApi, functionName)
        args['namespace'] = namespace

    if not 'create' in functionName:
        args['name'] = obj['metadata']['name']
    if 'delete' in functionName:
        from kubernetes.client.models.v1_delete_options import V1DeleteOptions
        obj = V1DeleteOptions()

    log.info('Kind %s, namespace %s, functionName %s, function %s', kind, namespace, functionName, function)
    return function(body=obj, **args)


def describe(obj):
    return "%s '%s'" % (obj['kind'], obj['metadata']['name'])

def camel2snake(string):
    string = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    string = re.sub('([a-z0-9])([A-Z])', r'\1_\2', string).lower()
    return string

