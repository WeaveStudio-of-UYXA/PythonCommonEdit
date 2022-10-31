from enum import Enum
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PyCE.CEFunction.CESettings import *
class CESettingsLine(QFrame):
    class Type(Enum):
        Unkown = 0
        ComboBox = 1
        LineEdit = 2
        TextEdit = 3
    __Type = Type.Unkown
    __CESettingsKey = ""
    def __init__(this, type:Type, parent:QWidget = None):
        super().__init__(parent)
        this.setParent(parent)
        this.setObjectName("CESettingsLine")
        this.TextLabel = QLabel(this)
        if type == this.Type.ComboBox:
            this.InputEdit = QComboBox(this)
        elif type == this.Type.LineEdit:
            this.InputEdit = QLineEdit(this)
        elif type == this.Type.TextEdit:
            this.InputEdit = QTextEdit(this)
        else:
            this.InputEdit = QLineEdit(this)

    def binding(this, CESettingsKey:str):
        if (CESettingsKey not in CESets.getKeys()):
            raise Exception("Exception:CESettingsList:Can not bind a CESettingsList object with CESettings system as '"+ CESettingsKey +"' could not be found in settings list.")
        this.__CESettingsKey = CESettingsKey
        value= CESets.valueOf(CESettingsKey)
        if (this.__Type == CESettingsLine.Type.LineEdit):
            this.InputEdit.setText(value)
        
