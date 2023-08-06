'''import BaseHTTPServer, SimpleHTTPServer
import ssl

if __name__ == "__main__":
    ssl_key = '/etc/letsencrypt/live/cloud.homevee.de/privkey.pem'
    ssl_cert = '/etc/letsencrypt/live/cloud.homevee.de/fullchain.pem'

    httpd = BaseHTTPServer.HTTPServer(('localhost', 9999),SimpleHTTPServer.SimpleHTTPRequestHandler)
    #httpd.socket = ssl.wrap_socket (httpd.socket,keyfile=ssl_key,certfile=ssl_cert, server_side=True)
    httpd.serve_forever()
'''

import socket
import traceback
from socket import AF_INET, SOCK_STREAM, SO_REUSEADDR, SOL_SOCKET, SHUT_RDWR
import ssl

KEYFILE = '/etc/letsencrypt/live/cloud.homevee.de/privkey.pem'
CERTFILE = '/etc/letsencrypt/live/cloud.homevee.de/fullchain.pem'

def echo_client(s):
    while True:
        data = s.recv(8192)
        print(data.decode("utf-8"))
        if data == b'':
            break
        s.send(b'This is a response.')
        print('Sendind: This is a response.')
        print('Connection closed')
    s.close()

def echo_server(address):
    s = socket.socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(1)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    s_ssl = ssl.wrap_socket(s, keyfile=KEYFILE, certfile=CERTFILE, server_side=True)

    while True:
        try:
            (c,a) = s_ssl.accept()
            print('Got connection', c, a)
            echo_client(c)
        except socket.error as e:
            traceback.print_exc()
            print('Error: {0}'.format(e))

echo_server((socket.gethostbyname('cloud.homevee.de'), 7778))