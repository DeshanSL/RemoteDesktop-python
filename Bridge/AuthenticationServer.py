import json
import win32security
import rsa


class Padding:
    def __init__(self, len):
        self.length = len
        self.Data = b''
        self.buff = b''

    def spacing(self, data_in):
        while len(data_in) % self.length != 0:
            data_in = data_in + b' '
        return data_in


class AuthenticateUsers:
    @staticmethod
    def Authenticate(username, domain, password):
        try:
            token = win32security.LogonUser(
                username,
                domain,
                password,
                win32security.LOGON32_LOGON_NETWORK,
                win32security.LOGON32_PROVIDER_DEFAULT)
            authenticated = bool(token)
        except:
            return None
        print("Authorized")
        return authenticated


class SecureLayer:
    def __init__(self, connection):
        self.__decryptedResponse = None
        self.connection = connection
        (self.PublicKey, self.__PrivateKey) = rsa.newkeys(1024)
        strKey = str(self.PublicKey)[10:-1]
        Spacing = Padding(2048)
        PublicKeyByte = Spacing.spacing(strKey.encode())
        self.connection.send(PublicKeyByte)
        print(self.PublicKey)

    def Decryption(self, JSON):
        self.__decryptedResponse = rsa.decrypt(JSON.strip(), self.__PrivateKey)
        print(self.__decryptedResponse)
        jsonString = self.__decryptedResponse.decode('utf-8').replace("'", '"').strip()
        print(jsonString)
        JSON = json.loads(jsonString)
        WindowsAuthentication = AuthenticateUsers.Authenticate(JSON['User'], 'Local', JSON['Password'])
        if WindowsAuthentication:
            print(JSON['Target'])
            return JSON['Target']
        else:
            print("None")
            return None

