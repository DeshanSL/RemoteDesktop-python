import threading
from win32api import GetSystemMetrics
from PIL import Image
import mouse

global W
global H
global CursorX
global CursorY
DisplayX = GetSystemMetrics(0)
DisplayY = GetSystemMetrics(1)


def Resize(Img):
    try:
        cursor = Image.open('cursor.png')
        CursorCC = Img.copy()
        CursorCC.paste(cursor, (CursorX, CursorY), cursor)
        Img = CursorCC
    except:
        Img = Img
    try:
        WindowSize = (W, H)
        RIMG = Img.resize(WindowSize)
        return RIMG
    except:
        return Img


def returnCurrentPointer():
    global CursorY, CursorX
    while True:
        currentPos = mouse.get_position()
        CursorX = currentPos[0]
        CursorY = currentPos[1]


PointerThread = threading.Thread(target=returnCurrentPointer).start()


def ReScaleCursorPosition(x, y):
    XRatio = DisplayX / W
    YRatio = DisplayY / H
    rX = x * XRatio
    rY = y * YRatio

    return rX, rY
