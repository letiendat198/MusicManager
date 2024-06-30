from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel


class HLine(QFrame):
    def __init__(self, parent=None):
        super(HLine, self).__init__(parent)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

class PlaylistSeperator(QHBoxLayout):
    def __init__(self, name, parent=None):
        super(PlaylistSeperator, self).__init__(parent)

        self.line = HLine()

        self.label = QLabel(name)
        self.font = QFont()
        self.font.setPointSize(10)
        self.label.setFont(self.font)
        self.label.setContentsMargins(0, 0, 5, 5)
        self.label.setWordWrap(True)
        self.label.setFrameShape(QFrame.NoFrame)
        self.label.setLineWidth(0)

        self.addWidget(self.label)
        self.addWidget(self.line)