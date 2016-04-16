#!/usr/bin/python
#
# Insert bank server code here.
#
import rpclib
import sys
from debug import *
from zoodb import *

class BankRpcServer(rpclib.RpcServer):
    def rpc_get_balance(self, username):
        db = bank_setup()
        person = db.query(Bank).get(username)
        if not person:
            return None
        return person.zoobars

    def rpc_set_balance(self, username, zoobars):
        db = bank_setup()
        person = db.query(Bank).get(username)
        if not person:
            return None
        person.zoobars = zoobars
        db.commit()
        return None

    def rpc_register(self, username):
        db = bank_setup()
        bank = db.query(Bank).get(username)
        if bank:
            return None
        newbank = Bank()
        newbank.username = username
        db.add(newbank)
        db.commit()
        return None

(_, dummy_zookld_fd, sockpath) = sys.argv

s = BankRpcServer()
s.run_sockpath_fork(sockpath)

