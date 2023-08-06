#SERVER

import socket
import cv2
import numpy as np
global s
#global clientsocket

host = 'localhost'
port = 5012

class sock():
    soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    '''
    soc.bind((host,port))
    soc.listen(5)
    (clientsocket, address) = soc.accept()
    '''


def sockCon():
    #s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.soc.bind((host,port))
    print 'waiting'
    sock.soc.listen(5)
    
    (clientsocket, address) = sock.soc.accept()
    print 'connection found!'
    return clientsocket
    

def recv_buff(sock,count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

def recv_data(clientsocket):

    try:
        length = recv_buff(clientsocket,20)
    
        stringData = recv_buff(clientsocket, int(length))
        return stringData
    except:
        print 'error recieving proper values'
    

def dec_data(data):
    np_img = np.fromstring(data,dtype='uint8')
    image = cv2.imdecode(np_img,1)
    return image
    
def display_img(clientsocket):
    while True:
        print 'displaying..'
        data = recv_data(clientsocket)
        image = dec_data(data)
        try:
            cv2.imshow('image',image)
        except:
            print "bad image"
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
        
            break
def main():
    while True:
        
        #cs = sockCon()
        cs = sockCon()
        try:
            display_img(cs)
        except:
            print 'error reading'

if __name__ == "__main__":
    main()
