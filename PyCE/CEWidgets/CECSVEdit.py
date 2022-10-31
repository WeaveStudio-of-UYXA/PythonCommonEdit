from PySide2.QtCore import * 
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class CECSVEdit(QTextEdit):
    lineCountChanged = Signal(int)
    def __init__(this, parent:QWidget=None):
        super().__init__(parent)
        this.setParent(parent)
        this.setObjectName("CECSVEdit")
        this.LineList = []

    def getLineCount(this)->int:
        Text = this.toPlainText()
        Enter = Text.count("\n")
        if (Text.rindex("\n") != len(Text)-1):
            Enter += 1
        return Enter

    def getLineReset(this):
        this.getLineStart = 0

    def getLines(this)->str:
        this.LineList = this.toPlainText().split("\n")
        return this.LineList




        

