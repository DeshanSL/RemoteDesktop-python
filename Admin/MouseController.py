import cv2
import queue

q = queue.Queue()


def mouse_coo(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        img_res_tpl = cv2.getWindowImageRect("URD Administrator", )

        X, Y, W, H = img_res_tpl
        pointerLocationAndwindow = (x, y, W, H)
        pointerLocationAndwindowSTR = str(pointerLocationAndwindow)
        q.put(pointerLocationAndwindowSTR)

    if event == cv2.EVENT_LBUTTONDOWN:
        click = "LD"
        q.put(click)
    if event == cv2.EVENT_LBUTTONDBLCLK:
        click = "2l"
        q.put(click)
    if event == cv2.EVENT_RBUTTONDOWN:
        click = "RD"
        q.put(click)
    if event == cv2.EVENT_LBUTTONUP:
        click = "LU"
        q.put(click)
    if event == cv2.EVENT_RBUTTONUP:
        click = "RU"
        q.put(click)
