# server

import socket
from threading import Thread

clients = {}

def report_clients():
    print('Active clients: ' + str(len(clients)))

def multicast(sendersocket, message):
    senderkey = str(sendersocket.getpeername())
    for key in clients:
        if key != senderkey:
            recvsocket = clients[key]
            recvsocket.send(message.encode())


def readsocket(socket):
    key = str(socket.getpeername())
    while True:
        data = socket.recv(512).decode()
        if not data:
            print('client exiting: ' + key)
            break        
        s = str(data)
        print(s)
        multicast(socket, s)
        
    socket.close()
    del clients[key]
    report_clients()

def startlistening():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('127.0.0.1',9999))
    serversocket.listen(5)
    print('listening')
    while True:
        (clientsocket, address) = serversocket.accept()
        print('accepted from ' + str(address))
        t = Thread(target=readsocket, args=(clientsocket,))
        key = str(clientsocket.getpeername())
        clients[key] = clientsocket
        report_clients()
        t.start()

if __name__ == '__main__':
    startlistening()
        