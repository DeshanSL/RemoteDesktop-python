import os
import sys
import time
import queue
from infi.systray import SysTrayIcon
import socket
import subprocess

CurrentStateQ = queue.Queue()


def sysTray():
    def UpdateHover(systray):
        Status = None
        while True:
            HostName = socket.gethostname()
            IP = socket.gethostbyname(HostName)

            try:
                CurrentState = CurrentStateQ.get(block=False)
                print(CurrentState)
                Status = CurrentState
            except:
                Status = Status
                pass

            systray.update(hover_text=f"{HostName}\n{IP}\n{Status}")
            time.sleep(1)

    def ExitService(systray):
        subprocess.run("taskkill /f /im URDClientService.exe", shell=True)

    def Restart(systray):
        sys.stdout.flush()
        os.execl(sys.executable, 'python', "URDClientService.py", *sys.argv[1:])

    menu_options = (("Restart", None, Restart), ("Quit URD Client", None, ExitService))
    systray = SysTrayIcon("icon.ico", "Connecting..", menu_options)
    systray.start()
    UpdateHover(systray)
