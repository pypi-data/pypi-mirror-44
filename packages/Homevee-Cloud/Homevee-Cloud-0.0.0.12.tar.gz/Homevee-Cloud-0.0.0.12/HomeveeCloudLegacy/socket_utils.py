#!/usr/bin/python
# -*- coding: utf-8 -*-
import base64
import hashlib
import json
import random
import traceback
import urllib2
import uuid
import os

BUFFER_SIZE = 64

END_OF_MESSAGE = '[END_OF_MESSAGE]'

def is_server_premium(remote_id, access_token):
    try:
        url = "http://cloud.homevee.de/server-api.php?action=ispremium&remoteid="+remote_id+"&accesstoken="+access_token
        contents = urllib2.urlopen(url).read()

        print contents

        if contents == "wrongcredentials":
            return None

        data = json.loads(contents)

        if 'is_premium' in data and data['is_premium'] is not None:
            return data['is_premium']
        else:
            return None
    except:
        traceback.print_exc()
        return None

def assign_cloud_to_remote_id(cloud, server_secret, remote_id, access_token):
    try:
        url = "http://cloud.homevee.de/server-api.php?action=assigncloudtoremoteid&remoteid="+remote_id+"&cloud="+cloud+"&secret="+server_secret+"&accesstoken="+access_token

        contents = urllib2.urlopen(url).read()

        if(contents == "wrongcredentials"):
            return False, False

        print "response: "+contents

        data = json.loads(contents)

        verified = data['verified']
        is_premium = data['is_premium']
        status = data['status']

        if status == "nopermission":
            return False, False

        return verified, is_premium

    except:
        traceback.print_exc()

    return False, False

def encrypt_data(data, private_key):
    private_key = ""
    return data

def decrypt_data(data, public_key):
    private_key = ""
    return data

def send_to_server(conn, text):
    len_send = conn.send(text+END_OF_MESSAGE)

    print "sending to local server: "+text

    result = ""

    while not result.endswith(END_OF_MESSAGE):
        result += conn.recv(BUFFER_SIZE)

    print "received from local server: "+result

    return result

def get_client_id(clients):
    i = 0
    while True:
        if i in clients:
            i += 1
        else:
            return i

def generate_server_credentials(db):
    remote_id = ""
    access_token = ""

    #generate random remote_id thats not in db
    with db:
        cur = db.cursor()

        lst = [random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in xrange(8)]
        id = "".join(lst)

        cur.execute("SELECT REMOTE_ID FROM SERVER_DATA WHERE REMOTE_ID = :id", {'id': id})
        data = cur.fetchone()
        if data is None:
            #no entry existing
            remote_id = id

    #generate access_token
    random_bytes = os.urandom(128)
    access_token = base64.b64encode(random_bytes).decode('utf-8')

    print remote_id


    # hash_password
    salt = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    t_sha = hashlib.sha512()
    t_sha.update(access_token + salt)
    hashed_token = base64.urlsafe_b64encode(t_sha.digest())

    save_server_access_token(remote_id, hashed_token, salt, db)

    return remote_id, access_token

    '''
        len_send = conn.send(text)
        
        data = conn.recv(8192)
        
        return data
    '''