import rsa
import json


class SecureLayer:
    def __init__(self, s, JSON, ServerKey):
        self.Socket = s
        self.JSON = JSON
        self.ServerKey = ServerKey.strip()
        print(self.JSON)

    def Encryption(self):
        jsonString = json.dumps(self.JSON).encode()
        KeyTuple = eval(self.ServerKey.decode())
        key, attr = KeyTuple
        ServerRSA = rsa.key.PublicKey(key, attr)
        EncryptedJSON = rsa.encrypt(jsonString, ServerRSA)
        print(EncryptedJSON)
        return EncryptedJSON
