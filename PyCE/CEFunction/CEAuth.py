from socket import *
import time
from PyCE.CEFunction.CESettings import *

class CEClient:
    def __init__(this):
        this.Size = 1024
        #this.Host = 'yxgeneral.cn'
        if (CESets.valueOf("Auth")=="__DEFAULT__"):
            this.Host = 'yxgeneral.cn'
        elif (CESets.valueOf("Auth")=="__LOCAL__"):
            this.Host = "127.0.0.1"
        else:
            this.Host = CESets.valueOf("Auth")
        
        this.Port = 41471
        this.Address = (this.Host, this.Port)
        this.Socket = socket(AF_INET, SOCK_STREAM)
        this.Socket.settimeout(5)
        
        
    def connectServer(this):
        try:
            this.Socket.connect(this.Address)
        except:
            print('C_SAT:未能连接到通信服务器')
            return False
        else:
            print("C_SAT:作为客户端建立通讯")
            return True

    def Send(this, str:str):
        this.Socket.send((str+"\n").encode("utf-8"))

    def Receive(this):
        return this.Socket.recv(this.Size).decode("utf-8")

    def __del__(this):
        this.Socket.close()

