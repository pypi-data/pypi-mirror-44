import socket
import ssl
import sys
import traceback

from HomeveeCloud.ClientThread import ClientThread


class HomeveeCloud():
    def __init__(self, server_secret, domain, port=7778, client_num=50, is_debug=False, buffer_size=64):
        self.domain = domain
        self.port = port
        self.server_secret = server_secret
        self.client_num = client_num
        self.is_running = False
        self.is_debug = is_debug
        self.buffer_size = buffer_size

    def server_is_running(self):
        return self.is_running

    def listen_for_requests(self, listening_socket):
        if(not self.is_debug):
            KEYFILE = '/etc/letsencrypt/live/' + self.domain + '/privkey.pem'
            CERTFILE = '/etc/letsencrypt/live/' + self.domain + '/cert.pem'

            print(KEYFILE)
            print(CERTFILE)

            listening_socket = ssl.wrap_socket(listening_socket, keyfile=KEYFILE, certfile=CERTFILE, server_side=True)

        conn, addr = listening_socket.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]))

        client_thread = ClientThread(conn, self.buffer_size, self.domain, self.server_secret)
        client_thread.process()

    def start_server(self):
        print("Starting Homevee-Server")

        listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            domain = "localhost"

            if(not self.is_debug):
                domain = socket.gethostbyname(self.domain)

            listening_socket.bind((domain, self.port))
        except socket.error as msg:
            print(sys.exit())

        listening_socket.listen(self.client_num)

        self.is_running = True

        while 1:
            try:
                self.listen_for_requests(listening_socket)
            except(ssl.SSLError):
                print("SSLError")
            except(socket.error):
                traceback.print_exc()
                #print("SocketError")
            except KeyboardInterrupt:
                print("CTRL-C => Exiting")
                break
            except:
                traceback.print_exc()

        self.is_running = False

        listening_socket.close()