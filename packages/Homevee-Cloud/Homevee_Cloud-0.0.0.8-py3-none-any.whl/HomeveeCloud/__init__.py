import json
import socket
import ssl
import sys
import traceback
from io import StringIO
from _thread import start_new_thread
from http.server import BaseHTTPRequestHandler

import HomeveeCloud
from HomeveeCloud import socket_utils, firebase_utils

SOCKET_MAP = {}

SERVER_SECRET = None
DOMAIN = None
PORT = 7778
CLIENT_NUM = 50
BUFFER_SIZE = 64
IS_DEBUG = False

def start(server_secret, domain, port=7778, client_num=50, is_debug=False, buffer_size=64):
    HomeveeCloud.SERVER_SECRET = server_secret
    HomeveeCloud.OMAIN = domain
    HomeveeCloud.PORT = port
    HomeveeCloud.CLIENT_NUM = client_num
    HomeveeCloud.IS_DEBUG = is_debug
    HomeveeCloud.BUFFER_SIZE = buffer_size

    print("Starting Homevee-Server")
    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        domain = "localhost"

        if(not is_debug):
            domain = socket.gethostbyname(DOMAIN)

        listening_socket.bind((domain, PORT))
    except socket.error as msg:
        print(sys.exit())

    listening_socket.listen(client_num)

    is_running = True

    while True:
        print(listening_socket.fileno())

        try:
            listen_for_requests(listening_socket)
        except(ssl.SSLError):
            print("SSLError")
        except(socket.error):
            #traceback.print_exc()
            print("SocketError")
        except KeyboardInterrupt:
            print("CTRL-C => Exiting")
            break
        except:
            traceback.print_exc()

    listening_socket.close()

def listen_for_requests(listening_socket):
    if(not IS_DEBUG):
        KEYFILE = '/etc/letsencrypt/live/' + DOMAIN + '/privkey.pem'
        CERTFILE = '/etc/letsencrypt/live/' + DOMAIN + '/cert.pem'

        listening_socket = ssl.wrap_socket(listening_socket, keyfile=KEYFILE, certfile=CERTFILE, server_side=True)

    conn, addr = listening_socket.accept()
    print('Connected with ' + addr[0] + ':' + str(addr[1]))

    start_new_thread(clientthread, (conn,))

def clientthread(conn):
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

            while(not data.endswith(socket_utils.END_OF_MESSAGE)):
                new_data =  conn.recv(BUFFER_SIZE)

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
                        #data = DATA_DICT['data']

                        verified, is_premium = socket_utils.assign_cloud_to_remote_id(DOMAIN, SERVER_SECRET, remote_id, access_token)

                        if verified:
                            print("id "+remote_id+" is verified")
                        else:
                            print("id "+remote_id+" is not verified")

                        if is_premium:
                            print("id "+remote_id+" is premium")
                        else:
                            print("id "+remote_id+" is not premium")

                        if verified:
                            #do stuff
                            SOCKET_MAP[remote_id] = {}
                            SOCKET_MAP[remote_id]['server'] = conn
                            SOCKET_MAP[remote_id]['clients'] = {}
                            send_to_client(json.dumps({'status': 'connectionok'}), conn, is_http)
                        else:
                            print("Not authorized")
                            result_dict = {'result': 'error'}
                            #len_send = conn.send(encrypt_data(json.dumps(result_dict)))
                            len_send = conn.send(json.dumps(result_dict))
                        return
                    except:
                        print("deleting remote id: "+remote_id)
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
                    except(KeyError):
                        if 'remote_id' not in DATA_DICT:
                            #remote_id nich angegeben
                            traceback.print_exc()
                            data = {'result': 'noremoteid'}
                            send_to_client(json.dumps(data), conn, False)
                        elif DATA_DICT['remote_id'] not in SOCKET_MAP:
                            #local server not connected
                            traceback.print_exc()
                            data = {'result': 'servernotconnected'}
                            send_to_client(json.dumps(data), conn, False)
                    return
                elif 'registration_ids' in DATA_DICT:
                    is_notification = True
                    print('Push-Notification Command')
                    #Send push notifications
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
            except:
                traceback.print_exc()
                if data == "registration":
                    #register server to cloud

                    #generate remote_id and access_token
                    #REMOTE_ID, ACCESS_TOKEN = socket_utils.generate_server_credentials(db)

                    #send_to_client(json.dumps({'result': 'registrationok', 'remote_id': REMOTE_ID, 'access_token': ACCESS_TOKEN}), conn, is_http)

                    send_to_client(json.dumps({'result': 'error', 'msg': 'registrationnotpossible'}), conn, is_http)

        except(socket.error):
            traceback.print_exc()
            break
        except:
            traceback.print_exc()
            send_to_client(json.dumps({'status': 'error'}), conn, is_http)

    # came out of loop
    conn.close()
    #db.commit()
    print("Verbindung beendet")

class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message

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

def get_socket(remote_id):
    if remote_id in SOCKET_MAP:
        return SOCKET_MAP[remote_id]['server']
    else:
        return None

def process_data(client_id, data):
    data['client_id'] = client_id

    try:
        if 'remote_id' in data:
            remote_id = data['remote_id']
        else:
            return None

        conn = get_socket(remote_id)

        if conn is None:
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
            print
            "websocket send"
            SOCKET_MAP[remote_id]['clients'][client_id]['server'].send_message_to_all(msg)
            # SOCKET_MAP[remote_id]['clients'][client_id]['server'].send_message(SOCKET_MAP[remote_id]['clients'][client_id]['connection'], msg)
        elif SOCKET_MAP[remote_id]['clients'][client_id]['type'] == "socket":
            print
            "socket send"
            send_to_client(msg, SOCKET_MAP[remote_id]['clients'][client_id]['connection'], False)
            SOCKET_MAP[remote_id]['clients'][client_id]['connection'].close()

        # delete client from socket_map
        del SOCKET_MAP[remote_id]['clients'][client_id]

        return
    except ValueError as e:
        traceback.print_exc()
        return

def send_to_client(data, conn, is_http):
    if not is_http:
        print("Sent Response: " + data)
    elif is_http:
        data = 'HTTP/1.1 200 OK\nContent-Type: text/html\n' + data + '\n'
        print("Sent HTTP-Response: " + data)

    # Prüfen, ob alle Daten gesendet wurden
    try:
        len_send = conn.send(data.encode('utf-8'))
        print("Data: " + str(len(data)) + " | Sent: " + str(len_send))
    except:
        traceback.print_exc()
        return

    # if(len_send is 0):
    #    send_to_client(json.dumps({'status': 'error'}), conn, is_http)