
import socket
import sys
import cPickle as pickle
from thread import *

HOST = 'localhost';
PORT = 8887;

DEBUG = False


# manages a connection from a client sending coordinates
class ClientConnection:


    def __init__(self):
        self.points = []
        
        
        
        
    def startServer(self):
        """ Starts the socket """
        # create the socket
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            print '!!! Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
            sys.exit();
            
        # bind socket
        try:
            self.socket.bind((HOST, PORT))
        except socket.error, msg:
            print '!!! Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit();
            
        # everything is ok - start listening
        self.socket.listen(10)
            
        # start new thread to listen for incomming connections
        start_new_thread(self.client_listener, ())
            
            
    def client_listener(self):
        """ Client listener to be in it's own thread """
        """ Only one client will be accepted """
        print "waiting for connection..."
        isClientConnected = False
        while not isClientConnected:
            try:
                conn, addr = self.socket.accept() # blocking until client connected 
                isClientConnected = True
            except socket.error as (errno, msg):
                if errno != 4:
                    raise
                print "error: " + str(errno)
         
        print "! Client Connected !"
        print "address: " + addr[0] + ':' + str(addr[1])

        
        while True:
            data = conn.recv(1024)
            data = data.strip()
            
            if len(data) > 1:
                self.points = pickle.loads(data)
                
                print self.points
                
        conn.close()




# TESTING CODE
if DEBUG:
    listener = ClientConnection()
    listener.startServer()
    
    print "testing server has started"
    
    while True:
        # wait for input
        data = 1

