from enum import Enum
from typing import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from win32 import win32api, win32gui
from win32.lib import win32con
from ctypes.wintypes import MSG, HWND

class CESelfWidgetTitleButton(Enum):
    Minimize = 0
    Maximize = 1
    Close = 2

class CEInsideStyle(Enum):
    WinUI = 0
    CEDayUI = 1
    CENoonUI = 2
    CENightUI = 3
    CEDarkUI = 4
    CETestUI = 5

class CESelfWidget_TitleFrame(QFrame):
    __TitleButton = [CESelfWidgetTitleButton.Minimize, CESelfWidgetTitleButton.Maximize, CESelfWidgetTitleButton.Close]
    __WindowFullSize = False
    __MaximizeButtonFullStyleSheet = ""
    __MaximizeButtonNormalStyleSheet = ""
    def __init__(this, parent:QWidget = None):
        super().__init__(parent)
        this.setParent(parent)
        this.TitleLabel = QLabel(this)
        this.TitleLabel.setObjectName("TitleLabel")
        this.minimumButton = QPushButton(this)
        this.minimumButton.setObjectName("MinButton")
        this.maximumButton = QPushButton(this)
        this.maximumButton.setObjectName("MaxButton")
        this.closeButton = QPushButton(this)
        this.closeButton.setObjectName("CloseButton")
        
        this.minimumButton.clicked.connect(this.__onMinimumButtonClicked__)
        this.maximumButton.clicked.connect(this.__onMaximumButtonClicked__)
        this.closeButton.clicked.connect(this.__onCloseButtonCliceked__)

    def __onMinimumButtonClicked__(this):
        win32gui.ShowWindow(this.parentWidget().winId(), win32con.SW_MINIMIZE)

    def __onMaximumButtonClicked__(this):
        if (this.__WindowFullSize):
            this.parentWidget().resize(1600, 900)
            this.__WindowFullSize = False
            this.maximumButton.setStyleSheet(this.__MaximizeButtonFullStyleSheet)
        else:
            this.parentWidget().setGeometry(QApplication.desktop().availableGeometry())
            this.__WindowFullSize = True
            this.maximumButton.setStyleSheet(this.__MaximizeButtonNormalStyleSheet)
    
    def __onCloseButtonCliceked__(this):
        this.parentWidget().close()
    
    @overload
    def setTitleButtonDisable(this, button:CESelfWidgetTitleButton):
        if (button in this.__TitleButton):
            this.__TitleButton.remove(button)
        this.__reloadTitleButton__()

    @overload
    def setTitleButtonDisable(this, buttonlist:List[CESelfWidgetTitleButton]):
        for i in buttonlist:
            if (i in this.__TitleButton):
                this.__TitleButton.remove(i)
        this.__reloadTitleButton__()

    @overload
    def setTitleButtonEnable(this, button:CESelfWidgetTitleButton):
        if (button not in this.__TitleButton):
            this.__TitleButton.append(button)
        this.__reloadTitleButton__()

    @overload
    def setTitleButtonEnable(this, buttonlist:List[CESelfWidgetTitleButton]):
        for i in buttonlist:
            if (i not in this.__TitleButton):
                this.__TitleButton.append(i)
        this.__reloadTitleButton__()

    def setSelfTitle(this, title:str):
        this.TitleLabel.setText(title)
        #this.setAlignment(Qt.AlignCenter)

    def setSelfTitleAlignment(this, alignment:Qt.Alignment):
        this.TitleLabel.setAlignment(alignment)

    def setSelfTitleStyleSheet(this, styleSheet:str):
        this.TitleLabel.setStyleSheet(styleSheet)

    def setSelfTitleFrameStyleSheet(this, styleSheet:str):
        this.setStyleSheet(styleSheet)
        
    def setSelfTitleFixedHeight(this, height:int):
        this.setFixedHeight(height)

    def setMinimumButtonStyleSheet(this, styleSheet:str):
        this.minimumButton.setStyleSheet(styleSheet)

    def setMaximumButtonFullStyleSheet(this, styleSheet:str):    
        this.__MaximizeButtonFullStyleSheet = styleSheet
        this.__setMaximumButtonStyleSheet__()

    def setMaximumButtonNormalStyleSheet(this, styleSheet:str):
        this.__MaximizeButtonNormalStyleSheet = styleSheet
        this.__setMaximumButtonStyleSheet__()

    def __setMaximumButtonStyleSheet__(this):
        if (this.__WindowFullSize):
            this.maximumButton.setStyleSheet(this.__MaximizeButtonNormalStyleSheet)
        else:
            this.maximumButton.setStyleSheet(this.__MaximizeButtonFullStyleSheet)

    def setCloseButtonStyleSheet(this, styleSheet:str):
        this.closeButton.setStyleSheet(styleSheet)

    def __reloadTitleButton__(this):
        if (CESelfWidgetTitleButton.Minimize in this.__TitleButton):
            this.minimumButton.show()
        else:
            this.minimumButton.hide()
        if (CESelfWidgetTitleButton.Maximize in this.__TitleButton):
            this.maximumButton.show()
        else:
            this.maximumButton.hide()
        if (CESelfWidgetTitleButton.Close in this.__TitleButton):
            this.closeButton.show()
        else:
            this.closeButton.hide()
    def mousePressEvent(this,event:QMouseEvent):
        if (this.TitleLabel.underMouse()):
            win32gui.ReleaseCapture()
            win32api.SendMessage(this.parentWidget().winId(), win32con.WM_SYSCOMMAND,win32con.SC_MOVE+win32con.HTCAPTION, 0)

    def resizeEvent(this, event:QResizeEvent):
        this.minimumButton.setGeometry(this.width()- this.height()*0.95/9*12*3, this.height()*0.025, this.height()*0.95/9*12, this.height()*0.95)
        this.maximumButton.setGeometry(this.width()- this.height()*0.95/9*12*2, this.height()*0.025, this.height()*0.95/9*12, this.height()*0.95)
        this.closeButton.setGeometry(this.width()- this.height()*0.95/9*12*1, this.height()*0.025, this.height()*0.95/9*12, this.height()*0.95)
        this.TitleLabel.setGeometry(QRect(0, 0, this.width(), this.height()))

class CESelfWidget_BackFrame(QFrame):
    __frameWidth__ = 20
    def __init__(this, parent:QWidget):
        super().__init__(parent)
        this.setParent(parent)

    def setSelfBackgroundStyleSheet(this, styleSheet:str):
        this.setStyleSheet(styleSheet)

    def setSelfGetResizeWidth(this, width:int):
        this.__frameWidth__ = width
        
    def nativeEvent(this, eventType:QByteArray, message):
        msg = MSG.from_address(message.__int__())
        if msg.message == win32con.WM_NCHITTEST:
            Gpos = QCursor.pos()
            CX = Gpos.x() - this.x()
            CY = Gpos.y() - this.y()
            L = CX < this.__frameWidth__
            R = CX > this.width() - this.__frameWidth__
            T = CY < this.__frameWidth__
            B = CY > this.height() - this.__frameWidth__
            if L and T:
                return True, win32con.HTTOPLEFT
            elif R and T:
                return True, win32con.HTTOPRIGHT
            elif L and B:
                return True, win32con.HTBOTTOMLEFT
            elif R and B:
                return True, win32con.HTBOTTOMRIGHT
            elif L:
                return True, win32con.HTLEFT            
            elif T:
                return True, win32con.HTTOP
            elif R:
                return True, win32con.HTRIGHT
            elif B:
                return True, win32con.HTBOTTOM        
        return QWidget.nativeEvent(this, eventType, message)

