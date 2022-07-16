class ReceiveData:
    def __init__(self, maxLength, socket):
        self.maxLength = maxLength
        self.lengthVar = maxLength
        self.Socket = socket
        self.ByteArray = b''

    def Recv(self):
        while True:
            Data = self.Socket.recv(self.lengthVar)
            self.ByteArray = self.ByteArray + Data
            if len(self.ByteArray) < self.maxLength:
                self.lengthVar = self.maxLength - len(self.ByteArray)
            else:
                break
        return self.ByteArray