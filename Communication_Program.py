import socket
import threading
connected = False  #messages only sent when connected
is_Server = False  #determines which socket is used for send function
global sock
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
global run_thread
run_thread = False

def connect(host, port): #actively connect to a specified server
    global connected
    global is_Server
    if connected == False:
        sock.connect((host, port))
        connected = True
        is_Server = False
    else:
        print('Already Connected to socket, try close()')



def listen(host, port): #listen/ bind to a socket and await a connection
    sock.bind((host, port))
    sock.listen(5)
    global is_Server
    is_Server = True
    global comm_sock
    a = 1
    while a == 1:
        comm_sock, addr = sock.accept()
        print('recieved communication from address %s' % (str(addr)))
        a = 2

    

def close(): #end communication
    global connected
    if connected == True:
        if is_Server == True:
            sock.close()
        else:
            comm_sock.close()
        connected = False
    else:
        print('Not connected to anything, can not disconnect')



def recieve(): #recieve message - intended to be run in a thread
    global comm_sock
    if is_Server == True:
        while run_thread == True:
            if len(comm_sock.recv(1024).decode()) > 0:
                print (comm_sock.recv(1024).decode())
    else:
        while run_thread == True:
            if len(sock.recv(1024).decode()) > 0:
                print (sock.recv(1024).decode())        



def send(): #send typed message - intended to be invoked by user
    global connected
    global comm_sock
    global is_Server
    if connected == True:
        message = input('Enter a message to be sent: \n')
        data = message.encode()
        if is_Server == True:
            comm_sock.send(data)
        else:
            sock.send(data)
    else:
        print('Not connected to anything, can not send message')

global recieve_thread
recieve_thread = threading.Thread(target=recieve, args = ())


def recieving_toggle(): #initiate thread for recieving messages
    global connected
    global recieve_thread
    if connected == True:
        if recieve_thread.is_alive() == False:
            run_thread = True
            recieve_thread.start()
        else:
            run_thread = False


def setup(host, port, server):
    if server == True:
        listen(host,port)        
    else:
        connect(host,port)

    recieving_toggle()


def shutdown():
    recieving_toggle()
    close()

            
    




