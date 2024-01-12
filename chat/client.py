import socket
import select
import threading

def receive_msg(socket):
    while True:
        try:
            data = socket.recv(512).decode()
            if data:
                msg = str(data)
                print(msg)
            else:
                print('socket seem closed. exiting.')
                break
        except:
            print('socket exception, exiting')
            break

def main():
    host = '127.0.0.1'
    port = 9999  # socket server port number
    print('type /quit to exit.')

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    t = threading.Thread(target=receive_msg, args=(client_socket,))
    t.start()

    while True:
        message = input(">")  # take input
        if message == '/quit':
            break
        client_socket.send(message.encode())
    
    client_socket.close()


if __name__ == '__main__':
    main()    
