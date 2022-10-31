from PySide2.QtCore import  *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from typing import *

class CEFreeButton(QFrame):
    selected = Signal(str)
    clicked = Signal(None)
    pressed = Signal(None)
    __NAHStyleSheet = ""
    __PressedStyleSheet = ""
    __InsideName = ""
    def __init__(this, parent:QWidget = None, RadioMode:bool = False):
        super().__init__(parent)
        this.setParent(parent)
        this.CurrentHLayout = QHBoxLayout()
        this.CurrentVLayout = QVBoxLayout()
        this.RadioMode = RadioMode
        this.InsiderImage = QLabel(this)
        this.InsiderImage.setObjectName("INSIDERIMAGE")

        this.InsiderLabel = QLabel(this)
        this.InsiderLabel.setObjectName("INSIDERLABEL")
        this.setAttribute(Qt.WA_Hover, True)

    def setText(this, text:str):
        this.InsiderLabel.setText(text)

    def setTextStyleSheet(this, style:str):
        this.InsiderLabel.setStyleSheet(style)

    def setNAHStyleSheet(this, style:str):
        this.setStyleSheet(style)
        this.__NAHStyleSheet= style

    def setPressedStyleSheet(this, style:str):
        this.__PressedStyleSheet= style

    def setPixmapStyleSheet(this, style:str):
        this.InsiderImage.setStyleSheet(style)

    def setTextAlignment(this, Alignment:Qt.Alignment):
        this.InsiderLabel.setAlignment(Alignment)

    def setCentralPixmap(this, url:str):
        this.InsiderImage.setStyleSheet("QLabel#INSIDERIMAGE{background-image: url("+url+");background-position: center;background-repeat: no-repeat;}")

    def click(this):
        this.pressed.emit()
        this.setStyleSheet(this.__PressedStyleSheet)
        this.clicked.emit()
        if (not this.RadioMode):
            this.setStyleSheet(this.__NAHStyleSheet)

    def radioModeReleaseButton(this):
        this.setStyleSheet(this.__NAHStyleSheet)

    def setInsideName(this, name:str):
        this.__InsideName=name

    def insideName(this):
        return this.__InsideName

    def mouseReleaseEvent(this, event:QMouseEvent):
        if (event.button() == Qt.LeftButton):
            this.clicked.emit()
            if (not this.RadioMode):
                this.setStyleSheet(this.__NAHStyleSheet)

    def mousePressEvent(this, event:QMouseEvent):
        if (event.button() == Qt.LeftButton):
            this.pressed.emit()
            this.setStyleSheet(this.__PressedStyleSheet)

    def mouseDoubleClickEvent(this, event:QMouseEvent):
        this.selected.emit(this.InsiderLabel.text())

    def text(this)->str:
        return this.InsiderLabel.text()

    def useAutoHorizontal(this):
        this.CurrentHLayout.addWidget(this.InsiderImage)
        this.CurrentHLayout.addWidget(this.InsiderLabel)
        this.setLayout(this.CurrentHLayout)

    def hideImage(this):
        this.InsiderImage.hide()



class CEFreeButtonGroup(QObject):
    Buttons:List[CEFreeButton]
    CurrentButton:CEFreeButton
    clicked = Signal()
    def __init__(this, parent:QWidget = None):
        super().__init__(parent)
        this.setParent(parent)
        this.Buttons = []
    
    def addCEFreeButton(this, Button:CEFreeButton):
        this.Buttons.append(Button)
        Button.clicked.connect(this.__changeCurrentButton)

    def __changeCurrentButton(this):
        this.CurrentButton = this.sender()
        for i in this.Buttons:
            if (i!=this.CurrentButton):
                i.radioModeReleaseButton()
        this.clicked.emit()