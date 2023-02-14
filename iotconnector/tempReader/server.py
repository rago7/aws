import socket
import http.server
import socketserver
from threading import *
from time import sleep
PORT = 8000

# Absolutely essential!  This ensures that socket resuse is setup BEFORE
# it is bound.  Will avoid the TIME_WAIT issue
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

    # os.chdir("/My/Webpages/Live/here.html")
    httpd.socket.listen(5)
    (clientsocket, address) = httpd.socket.accept()
    Temp = clientsocket.recv(1024)
    clientsocket.send(Temp)
    print(Temp)
    # httpd.serve_forever()
t = Thread(daemon=True,target=thread_tsk)
print(t.daemon)
# t.setDaemon(True)
print(t.daemon)
t.start()
# sleep(0.5)
print(t.is_alive())
t.run()
t.join()
print('after math')