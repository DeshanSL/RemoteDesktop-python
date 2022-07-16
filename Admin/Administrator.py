import sys
import threading
import cv2
import socket
import io
import numpy as np
from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget
import AuthenticationAdmin
import GUI
from MouseController import q, mouse_coo
import queue
from Utils import Padding
from Utils import ReadConfig
from Utils import PayloadReceiver

ImagesQ = queue.Queue()
CroppedImg = []


class Connection:
    def __init__(self):
        super().__init__()
        ServerIP, ServerPort = ReadConfig.ReadConf()
        self.sock = None
        self.TCP_IP = ServerIP
        self.TCP_PORT = ServerPort
        self.s = socket.socket()
        self.ServerKey = None

    def Establish(self):
        while True:

            self.s.connect((self.TCP_IP, self.TCP_PORT))
            print(self.s)
            print("connected")
            self.s.send(Padding.Padding.padd_message_byte("Admin".encode(), 256))
            while True:
                Receiver = PayloadReceiver.ReceiveData(2048, self.s)
                ServerKey = Receiver.Recv()
                if ServerKey:
                    break
            print(ServerKey)
            app = QApplication(sys.argv)
            window = QWidget()
            win = GUI.Window(window)
            window.show()
            print(win)
            app.exec_()

            JSON = GUI.JSONQueue.get(block=True)
            Authenticate = AuthenticationAdmin.SecureLayer(self.s, JSON, ServerKey)
            RequestJson = Authenticate.Encryption()
            self.s.send(Padding.Padding.padd_message_byte(RequestJson, 256))
            self.s.send("T".encode())
            return self.s

    def props(self):
        self.sock = self.s
        if self.sock is not None:
            return self.sock
        else:
            self.Establish()


class SendData:
    def __init__(self, q, s):
        self.q = q
        self.s = s

    def THREAD_1(self):
        while True:
            data = self.q.get(block=True)
            try:
                print(self.s)
                self.s.send(Padding.Padding.padd_message_byte(data.encode(), 256))
                print(data)
            except:
                continue

    def StartThread(self):
        threading.Thread(target=self.THREAD_1).start()


def rebuildImage(width, height):
    NewImage = Image.new('RGB', (width, height))
    place = 0
    for i in CroppedImg:
        try:
            img = i
            NewImage.paste(img, (0, place))
            place = place + 10
        except:
            continue
    return NewImage


def AppendTOARRAY():
    while True:
        try:
            ByteArray = ImagesQ.get(block=True)
            ArrayIndex = int(ByteArray[:16].strip())
            try:
                imageB = ByteArray[16:]
                image = Image.open(io.BytesIO(imageB))
                CroppedImg[ArrayIndex] = image
            except:
                imageB = ByteArray[16:]
                image = Image.open(io.BytesIO(imageB))
                CroppedImg.append(image)
        except:
            continue


def RecvFrames():
    while True:
        try:

            imgB = b''
            ChunksRecv = 0

            Receiver = PayloadReceiver.ReceiveData(256, s)
            numberOFCHUNKSB = Receiver.Recv()
            try:
                ChunksToRecv = numberOFCHUNKSB.decode()
            except:
                break
            while ChunksRecv < int(ChunksToRecv):
                Receiver = PayloadReceiver.ReceiveData(256, s)
                bArr = Receiver.Recv()
                ChunksRecv = ChunksRecv + 1
                imgB = imgB + bArr
            ImagesQ.put(imgB)
        except:
            continue


class MainWindow:
    @staticmethod
    def window():
        while True:
            try:
                X, Y, width, height = cv2.getWindowImageRect("URD Administrator", )
                if height < 100 or height < 50:
                    width = 150
                    height = 100
                image = rebuildImage(width, height)
                img_np = np.array(image)
                frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
                cv2.imshow("URD Administrator", frame)
                key = cv2.waitKey(1)
                if key == 27:
                    break
                if key != -1:
                    q.put(f'Key{key}')
            except:
                continue

        q.put("Connection_INTERUPPTED")
        print("Disconnected.")
        cv2.destroyAllWindows()
        sys.stdout.flush()


if __name__ == "__main__":
    Conn = Connection()

    Conn.Establish()
    s = Conn.props()
    cv2.namedWindow("URD Administrator", cv2.WINDOW_GUI_EXPANDED)
    cv2.setMouseCallback("URD Administrator", mouse_coo)
    StartSending = SendData(q, s)
    StartSending.StartThread()
    threading.Thread(target=AppendTOARRAY).start()
    threading.Thread(target=RecvFrames).start()
    MainWindow.window()
