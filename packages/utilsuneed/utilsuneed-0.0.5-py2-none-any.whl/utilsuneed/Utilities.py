import json
import socket
import multiprocessing
import serial
import thread

def printE(name="",message=""):
    print (" [ ",name," ] "," ",message)

def decode_to_json(command):
        status = 'empty'
        ret_val = {"status":status}
        if len(command)!=0:
            try:
                data = json.loads(command)
                status = data["status"]
                ret_val = data
            except:
                status = "data error"
        
        return ret_val,status

def encode_to_json(command):
        return json.dumps(command)

class COMMS:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_connection = None
    CLIENT = False
    SERVER = False


    def SERV_HOST(self,host,port):
        if not self.CLIENT:
            self.sock.bind((host, port))
            self.SERVER = True
        else:
            print "CLIENT IS {} , cannot create server".format(self.CLIENT)
        

    def SERV_NEW_CLI(self):
        self.sock.listen(1)
        self.client_connection, remoteAddr = self.sock.accept()

    def recv_buff(sock,count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

    def SERV_SEND(self,data):
        self.client_connection.send(data)

    def SERV_RECV(self,buffer = 3):
        return self.client_connection.recv()
        

    def CLIENT_CONNECT(self,host,port):
        if not self.SERVER:
            self.sock.connect((host,port))
            self.sock.settimeout(2)
            self.CLIENT = True
        else:
            print "SERVER IS {} , Cannot create client".format(self.SERVER)
        
    def CLIENT_SEND(self,command):
        self.sock.send(command)
    
    def CLIENT_RECV(self,buffer = 3):
        self.sock.recv(buffer)

    def SERV_order_syncronous(self,command):
        try:
            self.client_connection.send(str(len(command)).rjust(4))
            self.client_connection.send(command)
            buffer_recv = self.client_connection.recv(4)
            command = self.client_connection.recv(int(buffer_recv))
            self.ONLINE = True
            print command
            return command
        except:
            self.ONLINE = False
            return '{}'

    def CLIENT_order_synchronous(self,command):
        try:
            buffer_recv = self.sock.recv(4)
            data = self.sock.recv(int(buffer_recv))
            print data
            self.sock.send(str(len(command)).rjust(4))
            self.sock.send(command)

            self.ONLINE = True
            return data
        except:
            self.ONLINE = False
            return '{}'


class Vector3():
    
    _name_ = " [ VECTOR3 ] "
    x_MP = None
    y_MP = None
    z_MP = None
    _x = None
    _y = None
    _z = None
    multiprocessing = False


    def __init__(self,x = 0,y = 0,z = 0,multiprocessing = False):
        
        if multiprocessing:

            self.x_MP = MP.Value('f',x)
            self.y_MP = MP.Value('f',y)
            self.z_MP = MP.Value('f',z)

        self._x = x
        self._y = y
        self._z = z
        self.multiprocessing = multiprocessing 
        self.crossprocess_variable = None

    def __call__(self,x = 0,y = 0,z = 0,multiprocessing = False):
      
        if multiprocessing or self.multiprocessing:
            self.x_MP.value = x
            self.y_MP.value = y
            self.z_MP.value = z

        self._x = x
        self._y = y
        self._z = z

        self.multiprocessing = multiprocessing or self.multiprocessing

        return self

    @property
    def x(self):            
        if self.multiprocessing:
            return self.x_MP.value
        else:
            return self._x

    @property
    def y(self):
        if self.multiprocessing:
            return self.y_MP.value
        else:
            return self._y

    @property
    def z(self):
        if self.multiprocessing:
            return self.z_MP.value
        else:
            return self._z

    @x.setter
    def x(self,x):
        if self.multiprocessing:
            self.x_MP.value = x
        else:
            self._x = x

    @y.setter
    def y(self,y):
        if self.multiprocessing:
            self.y_MP.value = y
        else:
            self._y = y

    @z.setter
    def z(self,z):
        if self.multiprocessing:
            self.z_MP.value = z
        else:
            self._z = z

    def __add__(self, v):
        return Vector3(self.x + v.x, self.y + v.y, self.z + v.z)
    
    def __sub__(self, v):
        return Vector3(self.x - v.x, self.y - v.y, self.z - v.z)

    def __mul__(self, n):
        'n = SCALAR ONLY'
        return Vector3(self.x * n, self.y * n, self.z * n)

    def Dot(self,v):
        return Vector3(self.x * v.x , self.y * v.y ,self.z * v.z )

    def list(self):
        return self.x,self.y,self.z
        
    def copy(self,vec):
        self.x,self.y,self.z = vec.list()

    def copy_mp(self,obj):

        self.x_MP.value = obj._x
        self.y_MP.value = obj._y
        self.z_MP.value = obj._z
            

        self._x =  obj._x  #obj.x_MP.value
        self._y =  obj._y  #obj.y_MP.value
        self._z =  obj._z  #obj.z_MP.value

        self.multiprocessing = obj.multiprocessing

        return self

    def from_list(self,list):
        if len(list)>=3:
            self.x,self.y,self.z = list[0],list[1],list[2]
        else:
            print "[ VECTOR 3] : "

    def vector(self):
        '''
        return Numpy instance of the vector3 format
        '''
        return np.array([self.x,self.y,self.z])



class LOGGER:
    def __init__(self,filename = "LOGS/LOG_<timestamp>.csv"):

        if filename == "LOGS/LOG_<timestamp>.csv":
            stamp = time.ctime()
            stamp = '_'.join(stamp.split(":"))
            # jan print 'file stamp : ' ,stamp
            filename = "LOGS/LOG_"+stamp+".csv"
        self.filename = filename

    def log_all(self,parameter_list,attempts = 20):
        '''
        attempts = 0  // For infinite attempts , default attempts = 20 
        '''
        count = 0
        while True:
            
            try:
                with open(self.filename,mode = 'a') as file_obj:
                    for i in range(len(parameter_list)):
                        file_obj.write(str(parameter_list[i])+',')
                    file_obj.write('\r\n')
                break
            except:
                count+=1
                if count==attempts:
                    break


 
 
class SER_2_SOCK():

    host = 'localhost'
    port = 8001

    COMport = 'COM9'
    COMbaud = 115200

    buffSize= 4096
    serial_connect_timeouts = 1
    socket_connect_timeouts = 1
    
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


    ser_err = 0
    sock_err = 0

    def SETUP(self):
        ### create socket instance ###
        self.serverSocket.bind((host, port))
        self.serverSocket.listen(1)

    def CONNECT(self):
        ### create serial instance ###
        print("connect serial First , Waiting ...")

        while True:

            try:
                self.ser = serial.Serial(
                self.COMport,
                self.COMbaud,
                timeout=None,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                writeTimeout = 0,
                dsrdtr =False,
                rtscts =False,
                xonxoff =False)
                break
            except:
                print(self.ser.isOpen())
                print("Attempting to connect:",self.serial_connect_timeouts)
                time.sleep(1)
                self.serial_connect_timeouts+=1

        print("Connected Serial.")
        print("Connecting Socket...")
        while True:

            try:
                self.conn, self.remoteAddr = self.serverSocket.accept()
                break
            except:
                print("No request: waiting ...",self.socket_connect_timeouts)
                self.socket_connect_timeouts+=1
        print("Connected Socket.")


    def ser2sock(self,serial_h,socket_h):
        while True:
            self.data_ser = self.serial_h.read(32)
            self.socket_h.send(self.data_ser)
            

    def sock2ser(self,serial_h,socket_h):
        while True:
            self.data_sock = self.socket_h.recv(32)
            self.serial_h.write(self.data_sock)

    def START_SERVICE(self):
        self.s2s1 = thread.start_new_thread(self.ser2sock,(self,ser,conn))
        print('serial to socket stream: UP')
        self.s2s2 = thread.start_new_thread(self.sock2ser,(self,ser,conn))
        print('socket to serial stream: UP')
