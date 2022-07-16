import io
import os
import socket
import sys
import time
from PIL import ImageGrab
import funcy
import threading
import CursorController
import ResizeIMG
import queue
from Utils import Padding
import SysTrayIco
from Utils import ReadConfig
from Utils import PayloadReceiver

CurrentSendingQueue = []
q = queue.Queue()
SendingQUEUE = queue.Queue()
CroppedImages = []


class EstablishConnection:
    def __init__(self):
        ServerIP, ServerPort = ReadConfig.ReadConf()
        self.__Host = ServerIP
        self.__Port = ServerPort
        self.s = socket.socket()

    def Establish(self):
        while True:
            try:
                self.s.connect((self.__Host, self.__Port))
                self.s.send(Padding.Padding.padd_message_byte("Client".encode(), 256))
                print(self.s)
                print("connected")
                return self.s

            except:
                print("retrying..")
                time.sleep(2)


class Cursor:
    @staticmethod
    def ReceiveCursor():
        while True:
            Receiver = PayloadReceiver.ReceiveData(256, s)
            data = Receiver.Recv().strip()
            print(data)
            if str(data.decode()) == "!":
                s.send(" ".encode())
            if data.strip() == b'Connection_INTERUPPTED':
                SysTrayIco.CurrentStateQ.put("Connection_INTERUPPTED")
                print("Connection_INTERUPPTED")
                sys.stdout.flush()
                os.execl(sys.executable, 'python', "", *sys.argv[1:])
            else:
                CursorController.MouseDisplay(data.strip())
                print('C')


class Frames:
    def GrabFrames(self):
        print("sending..")
        while True:
            try:
                img = ImageGrab.grab()
            except:
                continue
            rIMG = ResizeIMG.Resize(img)
            self.GridImg(rIMG)

    @staticmethod
    def GridImg(img):
        CroppedHeight = 10
        left = 0
        top = 0
        ArrIndex = 0

        width, height = img.size
        while top <= height:
            cropped = img.crop((left, top, width, CroppedHeight))
            q.put((cropped, ArrIndex))
            top = top + 10
            CroppedHeight = CroppedHeight + 10
            ArrIndex = ArrIndex + 1


class PickImages:
    def __init__(self):
        self.CreateWorkers()

    def CreateWorkers(self):
        count = 0
        while count < 50:
            threading.Thread(target=self.CheckImg).start()
            count = count + 1

    def CheckImg(self):
        while True:
            img, ArrIndex = q.get(block=True)
            try:
                img1, index = CroppedImages[ArrIndex]
                if not img == img1:
                    try:
                        CurrentSendingQueue.index(ArrIndex)
                        pass
                    except:
                        CroppedImages[ArrIndex] = (img, ArrIndex)
                        SendingQUEUE.put((img, ArrIndex))
                        CurrentSendingQueue.append(ArrIndex)
                else:
                    pass
            except:
                CroppedImages.append((img, ArrIndex))
                SendingQUEUE.put((img, ArrIndex))
                CurrentSendingQueue.append(ArrIndex)


class StartService:
    @staticmethod
    def waitToAdmin(s):
        while True:
            time.sleep(1)
            print("waiting for confirmation..")
            SysTrayIco.CurrentStateQ.put("Available")
            try:
                confirmation = s.recv(1024)
                print(confirmation)
            except:
                sys.stdout.flush()
                os.execl(sys.executable, 'python', "", *sys.argv[1:])
                break
            print(confirmation)
            if str(confirmation.decode()) == "T":
                PickImages()
                threading.Thread(target=Send.SendTOSERVER).start()
                FrameManager = Frames()
                threading.Thread(target=FrameManager.GrabFrames).start()
                threading.Thread(target=Cursor.ReceiveCursor).start()
                break

            if str(confirmation.decode()) == "!":
                s.send(" ".encode())


class Send:
    @staticmethod
    def SendTOSERVER():
        SysTrayIco.CurrentStateQ.put("Busy")
        while True:
            byteArray = b''
            Image, ArrayIndex = SendingQUEUE.get(block=True)
            output = io.BytesIO()
            CurrentIndex = CurrentSendingQueue.index(ArrayIndex)
            CurrentSendingQueue.pop(CurrentIndex)
            Image.save(output, format="PNG")
            byteArray1 = output.getvalue()
            byteArray2 = Padding.Padding.padd_message(str(ArrayIndex)).encode()
            byteArray = byteArray2 + byteArray1

            chucks = list(funcy.chunks(256, byteArray))
            No_chunks = len(chucks)
            s.send(Padding.Padding.padd_message_byte(str(No_chunks).encode(), 256))
            for i in chucks:
                if len(i) < 256:
                    data = Padding.Padding.padd_message_byte(i, 256)
                else:
                    data = i

                s.send(data)


if __name__ == '__main__':
    Connections = EstablishConnection()
    s = Connections.Establish()
    if s:
        threading.Thread(target=SysTrayIco.sysTray).start()
        StartService.waitToAdmin(s)
