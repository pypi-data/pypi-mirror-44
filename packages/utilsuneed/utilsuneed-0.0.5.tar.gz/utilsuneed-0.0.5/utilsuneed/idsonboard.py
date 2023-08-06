#CLIENT

import cv2
import numpy as np
import socket
import Queue
import threading
import thread
import time
#global s
imgBuff = Queue.Queue()
cap = cv2.VideoCapture(0)

host = '192.168.1.4'
port = 5012

def buff():
    while True:
        imgBuff.put(cap.read())

class s:
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def encode_img(image):
    print 'encoding'
    encode_params = [int(cv2.IMWRITE_JPEG_QUALITY),90]
    retval,image  = cv2.imencode('.jpeg',image,encode_params)
    num_img = np.array(image)
    str_img = num_img.tostring()
    return str_img
    

def connect_serv():
    
    s.sock.connect((host,port))
    print 'connected'


def send_image(str_img):

    try:
        s.sock.send( str(len(str_img)).ljust(20))
        s.sock.send( str_img )
    except:
        print 'error sending'

def img_ids():
    while True:
        print 'from ids'
        #image = img_ids()
        _,image = cap.read()
        
        imgBuff.put(image,block = True,timeout = 0.6)


def capture_img():

    #if imgBuff.empty():
    #    time.sleep(0.6)
    #image = imgBuff.get(block = True,timeout = 0.6)
    _,image = cap.read()
    cv2.imshow('image',image)
    cv2.waitKey(1) & 0xFF
    str_img = encode_img(image)
    send_image(str_img)

def main():
    
    while True:
        capture_img()


#thread.start_new_thread(img_ids())

#thread.start_new_thread(img_ids())
#thread.start_new_thread(main())
#print 'accessing main'
def start(cam=0):
        cap = cv2.VideoCapture(cam)
        connect_serv()
        main()

if __name__=="__main__":
        start()
#main()
    
