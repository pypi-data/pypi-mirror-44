#!/usr/bin/python
# -*- coding: utf-8 -*-
import _ssl
import argparse
import base64
import hashlib
import json
import sys
from _thread import start_new_thread

import socket
import traceback
import ssl
from http.server import BaseHTTPRequestHandler
from io import StringIO

from HomeveeCloudLegacy import socket_utils, firebase_utils

HOST = 'free.cloud.homevee.de'  # Symbolic name meaning all available interfaces
PORT = 7778  # Arbitrary non-privileged port

SERVER_SECRET = "D5cj5JzZXD3Gw6KXdKTSVQY4BgkyTRxaCH2rrn48yuVDTZajmZ3sm4B7My2NT49dXqaWnSxwmFpJMPFyQy8CEjXZwv5rFEXPSsYEgxqSmTm7GfMGsaQpUmCSZ2gVJPNG"

BUFFER_SIZE = 64

test_speech = False

SOCKET_MAP = {}


class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message


# Function for handling connections. This will be used to create threads
def clientthread(conn):
    global HOST, PORT, SERVER_SECRET, BUFFER_SIZE
    # infinite loop so that function do not terminate and thread do not end.

    sent_data = None

    while True:

        is_http = False
        is_resend = False
        is_notification = False

        error = False

        try:
            # Receiving from client
            data = ""

            while (not data.endswith(socket_utils.END_OF_MESSAGE)):
                new_data = conn.recv(BUFFER_SIZE)

                data = data + new_data

            if data == "":
                conn.close()
                return

            print("")

            print("Received: " + data)

            if data.endswith(socket_utils.END_OF_MESSAGE):
                data = data[:-(len(socket_utils.END_OF_MESSAGE))]

            try:
                DATA_DICT = json.loads(data)

                if 'remote_id' in DATA_DICT and 'access_token' in DATA_DICT:
                    remote_id = DATA_DICT['remote_id']

                    try:
                        print('server connected')
                        access_token = DATA_DICT['access_token']
                        # data = DATA_DICT['data']

                        verified, is_premium = socket_utils.assign_cloud_to_remote_id(HOST, SERVER_SECRET, remote_id,
                                                                                      access_token)

                        if verified:
                            print("id " + remote_id + " is verified")
                        else:
                            print("id " + remote_id + " is not verified")

                        if is_premium:
                            print("id " + remote_id + " is premium")
                        else:
                            print("id " + remote_id + " is not premium")

                        if verified:
                            # do stuff
                            SOCKET_MAP[remote_id] = {}
                            SOCKET_MAP[remote_id]['server'] = conn
                            SOCKET_MAP[remote_id]['clients'] = {}
                            send_to_client(json.dumps({'status': 'connectionok'}), conn, is_http)
                        else:
                            print("Not authorized")
                            result_dict = {'result': 'error'}
                            # len_send = conn.send(encrypt_data(json.dumps(result_dict)))
                            len_send = conn.send(json.dumps(result_dict))
                        return
                    except:
                        print("deleting remote id: " + remote_id)
                        del SOCKET_MAP[remote_id]

                elif 'remote_id' in DATA_DICT:
                    print('client connected')
                    try:
                        client_id = socket_utils.get_client_id(SOCKET_MAP[DATA_DICT['remote_id']]['clients'])
                        SOCKET_MAP[DATA_DICT['remote_id']]['clients'][client_id] = {}
                        SOCKET_MAP[DATA_DICT['remote_id']]['clients'][client_id]['type'] = 'socket'
                        SOCKET_MAP[DATA_DICT['remote_id']]['clients'][client_id]['connection'] = conn
                        print("processing socket data...")
                        process_data(client_id, DATA_DICT)
                    except KeyError as e:
                        if 'remote_id' not in DATA_DICT:
                            # remote_id nich angegeben
                            traceback.print_exc()
                            data = {'result': 'noremoteid'}
                            send_to_client(json.dumps(data), conn, False)
                        elif DATA_DICT['remote_id'] not in SOCKET_MAP:
                            # local server not connected
                            traceback.print_exc()
                            data = {'result': 'servernotconnected'}
                            send_to_client(json.dumps(data), conn, False)
                    return
                elif 'registration_ids' in DATA_DICT:
                    is_notification = True
                    print('Push-Notification Command')
                    # Send push notifications
                    registration_ids = DATA_DICT['registration_ids']
                    message_data = json.loads(DATA_DICT['message_data'])

                    firebase_utils.send_notification(registration_ids, message_data)

                    send_to_client(json.dumps({'status': 'ok'}), conn, is_http)

                # Ist HTTP-Aufruf?
                try:
                    data = parse_http_headers(data)
                    is_http = True
                except AttributeError:
                    try:
                        data = json.loads(data)
                        print("Request is not in HTTP-Format")
                    except:
                        print("Data could not be parsed")
                        send_to_client(json.dumps({'status': 'error'}), conn, is_http)
                        error = True

                if 'resend' in data and data['resend'] is True:
                    # Daten erneut senden
                    print("Resend!")
                    is_resend = True
                    print(str(len(sent_data)) + " | " + sent_data)

                    send_to_client(sent_data[data['resendstart']:], conn, is_http)

                if not error and not is_resend and not is_notification:
                    if not is_resend and not is_notification:
                        reply = process_data(data)

                    if (reply is not None):
                        send_to_client(reply, conn, is_http)

                        sent_data = reply
                    else:
                        print("Error in reply")
                        send_to_client(json.dumps({'status': 'error'}), conn, is_http)

                    if not data:
                        break
            except Exception as e:
                traceback.print_exc()
                if data == "registration":
                    # register server to cloud

                    # generate remote_id and access_token
                    # REMOTE_ID, ACCESS_TOKEN = socket_utils.generate_server_credentials(db)

                    # send_to_client(json.dumps({'result': 'registrationok', 'remote_id': REMOTE_ID, 'access_token': ACCESS_TOKEN}), conn, is_http)

                    send_to_client(json.dumps({'result': 'error', 'msg': 'registrationnotpossible'}), conn, is_http)

        except socket.error as e:
            traceback.print_exc()
            break
        except Exception as e:
            traceback.print_exc()
            send_to_client(json.dumps({'status': 'error'}), conn, is_http)

    # came out of loop
    conn.close()
    # db.commit()
    print("Verbindung beendet")


def send_to_client(data, conn, is_http):
    if not is_http:
        print("Sent Response: " + data)
    elif is_http:
        data = 'HTTP/1.1 200 OK\nContent-Type: text/html\n' + data + '\n'
        print("Sent HTTP-Response: " + data)

    # Prüfen, ob alle Daten gesendet wurden
    try:
        len_send = conn.send(data)
        print("Data: " + str(len(data)) + " | Sent: " + str(len_send))
    except Exception as e:
        print(e.message)
        return

    # if(len_send is 0):
    #    send_to_client(json.dumps({'status': 'error'}), conn, is_http)


def parse_http_headers(data):
    if data.startswith("GET"):
        print("HTTP-GET-Request")
        request = HTTPRequest(data).path
        path, param_string = request.split('?', 1)
    elif data.startswith("POST"):
        print("HTTP-POST-Request")
        lines = data.split('\n')
        param_string = lines[-1]
    else:
        raise AttributeError

    params = {}

    param_fragments = param_string.split('&')

    for param in param_fragments:
        if '=' in param:
            key, value = param.split('=')
            params[key] = value

    return params


def listen_for_requests(s):
    global HOST, PORT, SERVER_SECRET, BUFFER_SIZE
    # wait to accept a connection - blocking call

    KEYFILE = '/etc/letsencrypt/live/' + HOST + '/privkey.pem'
    CERTFILE = '/etc/letsencrypt/live/' + HOST + '/cert.pem'

    # SSL aktivieren
    s = ssl.wrap_socket(s, keyfile=KEYFILE, certfile=CERTFILE, server_side=True)

    conn, addr = s.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))

    # print("SSL Socket")

    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread, (conn,))


def process_data(client_id, data):
    print("processing data...")

    data['client_id'] = client_id

    print(data)

    try:
        if 'remote_id' in data:
            remote_id = data['remote_id']
        else:
            print("remote_id not in data")
            return None

        conn = get_socket(remote_id)

        if conn is None:
            print("conn = None")
            return {'status': 'error', 'msg': 'servernotconnected'}

        try:
            msg = socket_utils.send_to_server(conn, json.dumps(data))
        except:
            data = {'error': 'servernotconnected'}
            msg = json.dumps(data)
            send_to_client(msg, SOCKET_MAP[remote_id]['clients'][client_id]['connection'], False)
            del SOCKET_MAP[remote_id]['clients'][client_id]
            return

        print('Sent to client with id ' + str(client_id) + ': ' + msg)

        if SOCKET_MAP[remote_id]['clients'][client_id]['type'] == "websocket":
            print("websocket send")
            SOCKET_MAP[remote_id]['clients'][client_id]['server'].send_message_to_all(msg)
            # SOCKET_MAP[remote_id]['clients'][client_id]['server'].send_message(SOCKET_MAP[remote_id]['clients'][client_id]['connection'], msg)
        elif SOCKET_MAP[remote_id]['clients'][client_id]['type'] == "socket":
            print("socket send")
            send_to_client(msg, SOCKET_MAP[remote_id]['clients'][client_id]['connection'], False)
            SOCKET_MAP[remote_id]['clients'][client_id]['connection'].close()

        # delete client from socket_map
        del SOCKET_MAP[remote_id]['clients'][client_id]

        return
    except ValueError as e:
        traceback.print_exc()
        print("error")
        return


def get_socket(remote_id):
    if remote_id in SOCKET_MAP:
        return SOCKET_MAP[remote_id]['server']
    else:
        return None


def main():
    parser = argparse.ArgumentParser(description='Homevee-Cloud for Servers')
    parser.add_argument('--domain', required=True, type=str,
                        help='Domain that the server is reachable under (z.B. free.cloud.homevee.de)')
    parser.add_argument('--port', default=7778, type=int, help='The Port the Homevee-Server should listen on')
    parser.add_argument('--server_secret', required=True, type=str,
                        help='The secret for communication with the main server')
    parser.add_argument('--max_clients', default=50, type=int, help='Number of clients simultaneously')
    parser.add_argument('--buffer_size', default=64, type=int, help='Buffer size for client communication')
    parser.add_argument('--debug', default=False, type=bool, help='Is the server in debug mode?')
    args = parser.parse_args()

    global HOST, PORT, SERVER_SECRET, BUFFER_SIZE
    HOST = args.domain
    PORT = args.port
    SERVER_SECRET = args.server_secret
    BUFFER_SIZE = args.buffer_size

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    # Bind socket to local host and port
    try:
        s.bind((socket.gethostbyname(HOST), PORT))
    except socket.error as msg:
        print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
        sys.exit()

    print('Socket bind complete')

    # Start listening on socket
    s.listen(50)
    print('Socket now listening')

    while 1:
        try:
            listen_for_requests(s)
        except ssl.SSLError as e:
            traceback.print_exc()
        except socket.error as e:
            traceback.print_exc()
        except KeyboardInterrupt:
            print("CTRL-C => Exiting")
            break
        except Exception as e:
            traceback.print_exc()

    s.close()