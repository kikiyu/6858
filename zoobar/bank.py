from zoodb import *
from debug import *

import time
import rpclib
import auth_client

def get_balance(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('get_balance', username=username)
        return ret

def set_balance(username, zoobars):
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('set_balance', username=username, zoobars=zoobars)
        return ret

def register(username):
    with rpclib.client_connect('/banksvc/sock') as c:
        ret = c.call('register', username=username)
        return ret

def transfer(sender, recipient, zoobars, token):
    if not auth_client.check_token(sender, token):
        raise AttributeError('bad token for transfer')

    persondb = person_setup()
    senderp = persondb.query(Person).get(sender)
    recipientp = persondb.query(Person).get(recipient)

    sender_balance = get_balance(sender) - zoobars
    recipient_balance = get_balance(recipient) + zoobars

    if sender_balance < 0 or recipient_balance < 0:
        raise ValueError()

    set_balance(sender, sender_balance)
    set_balance(recipient, recipient_balance)

    transfer = Transfer()
    transfer.sender = sender
    transfer.recipient = recipient
    transfer.amount = zoobars
    transfer.time = time.asctime()

    transferdb = transfer_setup()
    transferdb.add(transfer)
    transferdb.commit()

def balance(username):
    return get_balance(username)

def get_log(username):
    db = transfer_setup()
    return db.query(Transfer).filter(or_(Transfer.sender==username,
                                         Transfer.recipient==username))

