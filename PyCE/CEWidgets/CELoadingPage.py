from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class LoadingPage(QWidget):
    __CentralWidget__:QLabel
    __TitleLabel__:QLabel
    __InfoLabel__:QLabel
    def __init__(this,parent:QWidget = None)->None:
        super().__init__(parent)
        this.setParent(parent)
        this.setAttribute(Qt.WA_DeleteOnClose)
        this.resize(860,540)
        this.__CentralWidget__ = QLabel(this)
        this.__TitleLabel__ = QLabel(this)
        this.__InfoLabel__ = QLabel(this)

    def loadBackground(this, ImageDir:str)->None:
        this.__CentralWidget__.setStyleSheet("QLabel{border-image:url('"+ ImageDir +"');}")

    def setText(this, text:str)->None:
        this.__TitleLabel__.setText(text)

    def setTextStyleSheet(this, text:str)->None:
        this.__TitleLabel__.setStyleSheet(text)

    def checking(this)->None:
        qApp=QApplication.instance()
        if () : None
         
        else:
            qApp.exit(-1)


