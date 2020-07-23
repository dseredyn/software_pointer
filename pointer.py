#!/usr/bin/env python

# Software pointer for Linux with Qt5
# Author: Dawid Seredynski

import sys
import signal

from Xlib import display

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import QTimer, Qt

point_color = (255, 0, 0)
point_size = 20

class PointerApp:
    def __init__(self, point_color, point_size):
        self.app = QApplication(sys.argv)

        self.window = QWidget()
        self.window.setWindowTitle('PyQt5 Pointer App')
        self.window.setGeometry(100, 100, point_size+2, point_size+2)
        self.window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.window.setAttribute(Qt.WA_TranslucentBackground, True)
        
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush( QBrush(QColor(0,0,0,0)) )
        self.scene.update()
        self.scene.addEllipse(0,0,point_size,point_size, brush=QBrush(QColor(*point_color)))
        self.view = QGraphicsView(self.scene, parent=self.window)
        self.view.setStyleSheet("background-color:transparent;")
        self.view.show()

        self.timer = QTimer(self.app)
        self.timer.timeout.connect(self.updateFunc)

        signal.signal(signal.SIGINT, self.sigint_handler)

    def sigint_handler(*args):
        QApplication.quit()

    def spin(self):
        print ("Hit ctrl+c in the terminal to stop the pointer app.")
        self.window.show()
        self.timer.start(50)
        return self.app.exec_()

    def updateFunc(self):
        data = display.Display().screen().root.query_pointer()._data
        self.window.move(data["root_x"]+5, data["root_y"]+5)

app = PointerApp(point_color, point_size)
sys.exit(app.spin())
