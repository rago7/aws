import socket
import http.server
import socketserver
from threading import *
from time import sleep
PORT = 8000


def thread_tsk():
    # sleep(2)
    Temp = 0
    class MyTCPServer(socketserver.TCPServer):
        def server_bind(self):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print(self.server_address)
            self.socket.bind(self.server_address)

    Handler = http.server.SimpleHTTPRequestHandler

    httpd = MyTCPServer(("192.168.1.103", PORT), Handler)

    httpd.socket.listen(5)
    (clientsocket, address) = httpd.socket.accept()
    Temp = clientsocket.recv(1024)
    clientsocket.send(Temp)
    print(Temp)
    # httpd.serve_forever()
t = Thread(daemon=True,target=thread_tsk)
t.start()
# sleep(0.5)
# print(t.is_alive())
t.run()
# t.join()
print('after math')