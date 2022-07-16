import keyboard


def SelectKEY(value):
    try:
        if int(value) == 13:
            keyboard.press_and_release('enter')
        else:
            keyboard.write(chr(int(value)))
            print(chr(int(value)))
    except:
        pass