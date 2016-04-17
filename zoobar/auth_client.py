from debug import *
from zoodb import *
import rpclib

def login(username, password):
    ## Fill in code here.
    with rpclib.client_connect('/authsvc/sock') as c:
        ret = c.call('login', username=username, password=password)
        return ret

def register(username, password):
    ## Fill in code here.
    with rpclib.client_connect('/authsvc/sock') as c:
        ret = c.call('register', username=username, password=password)
        return ret

def check_token(username, token):
    ## Fill in code here.
    with rpclib.client_connect('/authsvc/sock') as c:
        ret = c.call('check_token', username=username, token=token)
        return ret

def get_token(username):
    ## Fill in code here.
    with rpclib.client_connect('/authsvc/sock') as c:
        ret = c.call('get_token', username=username)
        return ret
