import datetime
import socket
import sys
import threading
import time
from Utils import Padding as Pd
import queue
from Utils import ReadConfig
from AuthenticationServer import SecureLayer

InactiveConnections = []
IP_List = []
Admin = []
Client = []
ClientIP_List = []
AllConnections = []
AdminsQueue = queue.Queue()


class BridgeConnections:
    def __init__(self, Admin, Target):

        self.ByteArray = b''
        self.Data = b''
        self.ArrayLength = 256
        self.Admin = Admin
        self.Client = Target
        print(self.Admin)
        print(self.Client)
        threading.Thread(target=self.Forward).start()
        threading.Thread(target=self.Reverse).start()

    @classmethod
    def Confirmation(cls):
        pass

    def WriteConnectionLogs(self):
        CurrentDate = datetime.datetime.now()
        Record = Pd.Padding.padd_message_byte(str(self.Admin).encode(), 18).decode() + "-->" + Pd.Padding.padd_message_byte(str(self.Client).encode(), 18).decode() + "|  " + Pd.Padding.padd_message_byte(
            str(CurrentDate).encode(), 32).decode() + "|"

        with open("Connection_History.txt.txt", "r") as txt:
            data = txt.read()

        AddCurrentRecord = f"{Record}\n" + data

        with open("Connection_History.txt.txt", "w") as txt:
            txt.writelines(AddCurrentRecord)


    @classmethod
    def TerminateClient(cls, Connection):
        Pad = Padding(256)
        Connection.send(Pad.spacing(b'Connection_INTERUPPTED'))
        print("Connection Terminated")

    def Forward(self):
        #self.WriteConnectionLogs()
        while True:
            try:
                Data = self.Client.recv(256)
            except:
                threading.Thread(target=self.TerminateClient(self.Client))
                break
            try:
                self.Admin.send(Data)
            except:
                threading.Thread(target=self.TerminateClient(self.Client))
                break
        print("End.")

    def Reverse(self):
        while True:
            try:
                Data = self.Admin.recv(256)
            except:
                threading.Thread(target=self.TerminateClient(self.Client))
                break
            try:
                self.Client.send(Data)
            except:
                threading.Thread(target=self.TerminateClient(self.Client))
                break


class CreateSocket:
    def __init__(self):
        ServerIP, ServerPort = ReadConfig.ReadConf()
        self.__Host = ServerIP
        self.__Port = ServerPort
        self.sock = socket.socket()

    def SockBind(self):
        try:
            self.sock.bind((self.__Host, self.__Port))
            self.sock.listen(5)
            print("Listening..")
            return self.sock
        except socket.error as er:
            print("ERROR: ", er)


class Padding:
    def __init__(self, len):
        self.length = len
        self.Data = b''
        self.buff = b''

    def spacing(self, data_in):
        while len(data_in) % self.length != 0:
            data_in = data_in + b' '
        return data_in

    def PaddedMessageReceiver(self, Connection):
        while True:
            try:
                self.buff = Connection.recv(self.length)
                self.Data = self.Data + self.buff
                if len(self.buff) < self.length:
                    self.length = self.length - len(self.buff)
                else:
                    return self.Data.strip()
            except:
                print("Connection dropped")
                return None


class ReceiveData:
    def __init__(self, maxLength, socket):
        self.maxLength = maxLength
        self.lengthVar = maxLength
        self.Socket = socket
        self.ByteArray = b''

    def Recv(self):
        while True:
            print("Receiver Started.")
            Data = self.Socket.recv(self.lengthVar)

            self.ByteArray = self.ByteArray + Data
            if len(self.ByteArray) < self.maxLength:
                self.lengthVar = self.maxLength - len(self.ByteArray)
            else:
                break
        return self.ByteArray.strip()


class AdminManager:
    @staticmethod
    def CreateThreads():
        print("Threading Service started.. ")
        while True:
            print("Waiting for the queue...")
            AdminConnection = AdminsQueue.get()
            print(AdminConnection)
            try:
                threading.Thread(target=Receivers.StartCommunication, args=(AdminConnection,)).start()
                print("Listening to Admin Connection ")
            except:
                pass


def testService(connection, ):
    print("receiving service")
    while True:
        Recv = ReceiveData(256, connection)
        Message = Recv.Recv()
        print(Message)


class Receivers:
    @staticmethod
    def SetRole(connection, IP):
        print("Receiving.")
        Recv = ReceiveData(256, connection)
        Message = Recv.Recv()
        print(Message)
        if Message.decode() == "Client":
            Client.append(connection)
            ClientIP_List.append(IP)
            RefreshConnections.refresh_conns()
            print("Client Added")
            Receivers.WriteLogs(IP, "Client")
        if Message.decode() == "Admin":
            Admin.append(connection)
            AdminsQueue.put(connection)
            print("Admin Added")
            Receivers.WriteLogs(IP, "Administrator")
            RefreshConnections.refresh_conns()
        if Message.decode() == "Service":
            threading.Thread(target=testService, args=(connection,)).start()

    @staticmethod
    def StartCommunication(connection, ):
        Authentication = SecureLayer(connection)
        Recv = Padding(256)
        EncryptedJSON = Recv.PaddedMessageReceiver(connection)
        print("JSON:")
        JSON = Authentication.Decryption(EncryptedJSON)
        print(JSON)
        ip = socket.gethostbyname(JSON)
        TargetIndex = ClientIP_List.index(ip)
        ClientConnection = Client[TargetIndex]
        if ClientConnection:
            del Client[TargetIndex]
            del ClientIP_List[TargetIndex]
            threading.Thread(target=BridgeConnections, args=(connection, ClientConnection)).start()

    @staticmethod
    def WriteLogs(IP, UserType):
        CurrentDate = datetime.datetime.now()
        Record = Pd.Padding.padd_message_byte(str(IP).encode(), 18).decode() + "|  " + Pd.Padding.padd_message_byte(str(CurrentDate).encode(), 32).decode() + "|  " + Pd.Padding.padd_message_byte(str(UserType).encode(), 16).decode() + "|"
        with open("Logs.txt", "r") as txt:
            data = txt.read()

        AddCurrentRecord = f"{Record}\n" + data

        with open("Logs.txt", "w") as txt:
            txt.writelines(AddCurrentRecord)


class Connections(CreateSocket):
    def __init__(self):
        super().__init__()
        self.addr = None
        self.conn = None
        self.socket = self.SockBind()

    def acceptConnections(self):
        for conns in InactiveConnections:
            conns.close()

        del InactiveConnections[:]
        del IP_List[:]

        while True:
            try:
                self.conn, self.addr = self.socket.accept()
                InactiveConnections.append(self.conn)
                IP_List.append(self.addr[0])
                AllConnections.append(self.conn)
                threading.Thread(target=Receivers.SetRole, args=(self.conn, self.addr[0])).start()
                print("Setting up Role..")
                self.socket.setblocking(True)

            except:
                time.sleep(1)
                print("Connection error..")

    def thread(self):
        threading.Thread(target=self.acceptConnections).start()


class RefreshConnections:
    @staticmethod
    def refresh_conns():
        for i, conn in enumerate(Client):
            try:
                dummy = '!'
                conn.send(dummy.encode())
                print(conn)
                conn.recv(20480)
            except:
                del Client[i]
                del ClientIP_List[i]


class Registration:
    pass


if __name__ == "__main__":
    Connections = Connections()
    Connections.thread()
    sock = Connections.socket
    AdminManager.CreateThreads()
