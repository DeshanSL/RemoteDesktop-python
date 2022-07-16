from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QGridLayout, QLineEdit, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar
import sys
import queue

JSONQueue = queue.Queue()


class Window:
    def __init__(self, window):
        self.window = window
        self.window.setWindowTitle('URD Administrator')
        self.window.setWindowIcon(QIcon("icon.ico"))
        self.window.setGeometry(700, 400, 500, 200)
        self._grid()

    def ReturnValues(self):
        JSON = {"User": self.User.text(), "Password": self.Password.text(), "Target": self.Computer.text()}
        JSONQueue.put(JSON)
        print(JSON)

    def _grid(self):
        grid = QGridLayout()
        grid.addWidget(QLabel('Computer: '), 1, 0)
        self.Computer = QLineEdit()
        grid.addWidget(self.Computer, 1, 1)
        grid.addWidget(QLabel('User: '), 2, 0)
        self.User = QLineEdit()
        grid.addWidget(self.User, 2, 1)
        grid.addWidget(QLabel('Password: '), 3, 0)
        self.Password = QLineEdit()
        self.Password.setEchoMode(QLineEdit.Password)
        grid.addWidget(self.Password, 3, 1)
        self.Connect = QPushButton('Connect')
        self.Connect.clicked.connect(self.ReturnValues)
        self.Connect.clicked.connect(self.window.close)
        grid.addWidget(self.Connect, 4, 1)

        self.close = QPushButton('Close')
        self.close.clicked.connect(self.window.close)
        grid.addWidget(self.close, 4, 0)
        self.window.setLayout(grid)

    def _createMenu(self):
        self.menu = self.window.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.window.close)

    def _createToolBar(self):
        tools = QToolBar()
        self.addToolBar(tools)
        tools.addAction('Exit', self.close)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("I'm the Status Bar")
        self.setStatusBar(status)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    win = Window(window)
    window.show()
    sys.exit(app.exec_())
