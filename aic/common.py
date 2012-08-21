'''
Created on August 21, 2012

@author: Justin Hammond, Rackspace Hosting
'''

_version = 'ws.v1'

_apimap = {
    'login': 'login',
    'logout': 'logout',
    'schema' : 'schema',
    'readMethod' : 'doc/method',
    'readSchema' : 'schema',
    'getMethodURIs' : 'doc/method',
    'manual' : 'doc/reference',
    'controlCluster' : 'control-cluster',
}


def apimap(method):
    if not method in _apimap:
        raise TypeError('400',"(%s) is an unsupported command" % method)
    uri  = "/%s/%s" % (_version, _apimap[method])
    return uri