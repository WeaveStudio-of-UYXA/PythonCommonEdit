from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import sys
from typing import *
from PyCE.CEFunction.CELanguage import *
from PyCE.CEFunction.CEDirProtect import *
from PyCE.CEFunction.CESettings import *

#CEMain can be used to quickly and systematically initialize the basic modules in CE to start the application
class CEMain:
    """
    The user must implement the pure virtual functions :\n
    doPreSet(None)->None \n
    main(List[str])->int \n
    Use 'this' instead of 'self' as a pointer to the class \n
    this.qApp is a QApplication instance \n
    this.Setdict can be used to set the initial value of CESettings in doPreSet() \n 
    """
    qApp = None
    SetDict = {} 
    def __init__(this)->int:
        argv = sys.argv
        this.qApp = QApplication(argv)
        this.doPreSet()
        CEDirChc.check(CEDirCheck.whenFailed.doRepairWithWarning)
        CESets.setKVPair(this.SetDict)
        CESets.setBeyondPolicy(CESettings.WhenBeyond.doException)
        CESets.loadSettings()
        CELangSys.setName(CELanguage.fromStr(CESets.valueOf("Language")))
        CELangSys.setPath(".\\Users_Data\\language")
        CELangSys.load()

        a=this.main(argv)
        CESets.save()
        CELangSys.develop()
        sys.exit(a)

