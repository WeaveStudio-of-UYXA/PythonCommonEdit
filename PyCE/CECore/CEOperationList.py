#This file contains an Operation Manage System,which can provide developers with a simple way of building CtrlZ in their program
#The CEOperationSystem should be applied in such a way that an instance of the class CEOperationPort is established in the class 
#(or the relevant code outside the class) where the user operation needs to be saved.
#CEOperationManager itself has a global instance, CEOpeMng. 
#You can directly add the CEOperationPort instance to the global manager instance. 
#CEOperation depends on the objectname of QT to identify the control. 
# Therefore, the objectname must be set for the QT control and the parent object of the control that included in CEOperation.
import struct
from PySide2.QtCore import *

class CEOperationStruct:
    None
    
class CEOperationPort:
    EnvObject:QObject
    def __init__(this, Env:QObject):
        this.EnvObject = Env
        None

    

class CEOperationManager:
    def __init__(this):
        None