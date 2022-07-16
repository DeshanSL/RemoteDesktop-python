import mouse
import win32api
import KeyboardController
import ResizeIMG


def MouseDisplay(arg):
    data = arg
    global x, y

    if data.decode() == "1":
        mouse.click('middle')

    if data.decode() == "2l":
        mouse.double_click(button="left")

    if data.decode() == "LD":
        mouse.press(button='left')

    if data.decode() == "RD":
        print("RightDown")
        mouse.press(button='right')

    if data.decode() == "LU":
        print("LeftUP")
        mouse.release(button='left')

    if data.decode() == "RU":
        print("RightUP")
        mouse.release(button='right')

    if data.decode()[:3] == "Key":
        KeyboardController.SelectKEY(data.decode()[3:])

    else:
        try:
            Position = eval(data)

            x, y, W, H = Position
            ResizeIMG.W = W
            ResizeIMG.H = H
            rX, rY = ResizeIMG.ReScaleCursorPosition(x, y)
            ResizeIMG.CursorX = int(rX)
            ResizeIMG.CursorY = int(rY)
            win32api.SetCursorPos((int(rX), int(rY)))
        except:
            pass
