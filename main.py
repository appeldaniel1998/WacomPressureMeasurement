import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pandas as pd


class TabletSampleWindow(QWidget):
    def __init__(self, parent=None):
        super(TabletSampleWindow, self).__init__(parent)
        self.pen_is_down = False
        self.pen_x = 0
        self.pen_y = 0
        self.pen_pressure = 0
        self.lines = []
        self.text = ""
        # Resizing the sample window to full desktop size:
        frame_rect = app.desktop().frameGeometry()
        width, height = frame_rect.width(), frame_rect.height()
        self.resize(width, height)
        self.move(-9, 0)
        self.data = []
        self.setWindowTitle("Sample Tablet Event Handling")

    def tabletEvent(self, tabletEvent):
        self.pen_x = tabletEvent.pos().x()
        self.pen_y = tabletEvent.pos().y()
        self.pen_pressure = int(tabletEvent.pressure() * 100)
        print("Tablet event: ", tabletEvent.type(), " at ", self.pen_x, ", ", self.pen_y, " pressure: ", self.pen_pressure)
        if tabletEvent.type() == QTabletEvent.TabletPress:
            self.pen_is_down = True
            self.text = "TabletPress event"
            # self.lines = []  # clear the list of lines
            self.lines.append((0, 0))
        elif tabletEvent.type() == QTabletEvent.TabletMove:
            if self.pen_is_down:
                self.text = "TabletMove event"
                self.lines.append((self.pen_x, self.pen_y))  # add the current point to the list of lines
                self.data.append((self.pen_x, self.pen_y, tabletEvent.pressure(), QDateTime.currentDateTime().toString(Qt.ISODate)))
        elif tabletEvent.type() == QTabletEvent.TabletRelease:
            self.pen_is_down = False
            self.text = "TabletRelease event"
        self.text += " at x={0}, y={1}, pressure={2}%,".format(self.pen_x, self.pen_y, self.pen_pressure)
        if self.pen_is_down:
            self.text += " Pen is down."
        else:
            self.text += " Pen is up."
        tabletEvent.accept()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        for i in range(len(self.lines) - 1):
            p1 = QPoint(self.lines[i][0], self.lines[i][1])
            p2 = QPoint(self.lines[i + 1][0], self.lines[i + 1][1])
            if not ((self.lines[i][0] == 0 and self.lines[i][1] == 0) or (self.lines[i + 1][0] == 0 and self.lines[i + 1][1] == 0)):
                painter.drawPoint(p2)
                painter.drawLine(p1, p2)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def save_data(self):
        df = pd.DataFrame(self.data, columns=['X Value', 'Y Value', 'Pressure', 'Timestamp'])
        try:
            df.to_csv('tablet_data.csv')
        except:
            print("Error saving data")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainform = TabletSampleWindow()
    mainform.show()
    app.exec_()
    mainform.save_data()
