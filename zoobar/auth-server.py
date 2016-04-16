#!/usr/bin/python

import rpclib
import sys
import pbkdf2
import auth
import bank
from debug import *
from zoodb import *

class AuthRpcServer(rpclib.RpcServer):
    ## Fill in RPC methods here.
    def rpc_login(self, username, password):
        db = cred_setup()
        cred = db.query(Cred).get(username)
        if not cred:
            return None
        password = unicode(pbkdf2.PBKDF2(password, cred.salt).hexread(32))
        if cred.password == password:
            return auth.newtoken(db, cred)
        else:
            return None

    def rpc_register(self, username, password):
        db = cred_setup()
        cred = db.query(Cred).get(username)
        if cred:
            return None
        newcred = Cred()
        newcred.username = username
        newcred.salt = os.urandom(8).encode('base-64')
        newcred.password = unicode(pbkdf2.PBKDF2(password, newcred.salt).hexread(32))
        db.add(newcred)
        db.commit()

        db_person = person_setup()
        person = db_person.query(Person).get(username)
        newperson = Person()
        newperson.username = username
        db_person.add(newperson)
        db_person.commit()

        bank.register(username)
        return auth.newtoken(db, newcred)
    
    def rpc_check_token(self, username, token):
        db = cred_setup()
        cred = db.query(Cred).get(username)
        if cred and cred.token == token:
            return True
        else:
            return False

(_, dummy_zookld_fd, sockpath) = sys.argv

s = AuthRpcServer()
s.run_sockpath_fork(sockpath)
