#This file provides a path checking system, which can help check whether several paths required by the program are complete, 
#And can make certain responses as needed, such as silent completion, raising exceptions, etc.
from typing import *
from enum import *
import os
strlist=List[str]


class CEDirCheck:
    class whenFailed(Enum):
        unknown = 0,
        doException = 1
        doRepairWithWarning = 2
        doRepairWithSlience = 3

    __ProPATH__=[""]
    def __init__(this, DirList:strlist = [""])->None:
        this.__ProPATH__ = DirList

    def setDir(this, SingleDir:str)->None:
        this.__ProPATH__ = [SingleDir]

    def setDirList(this, DirList:strlist)->None:
        this.__ProPATH__ = DirList

    def addDir(this, SingleDir:str)->None:
        this.__ProPATH__ += [SingleDir]

    def addDirList(this, DirList:strlist)->None:
        this.__ProPATH__ += DirList

    def check(this, whenFailed:whenFailed = whenFailed.doRepairWithSlience)->None:
        for Path in this.__ProPATH__:
            if (not os.path.exists(Path)):
                if (whenFailed == this.whenFailed.doException):
                    raise Exception("Exception:CEDirCheck:The specified Directory '"+ Path +"' could not be found")
                elif (whenFailed == this.whenFailed.doRepairWithSlience):
                    os.makedirs(Path)
                elif (whenFailed == this.whenFailed.doRepairWithWarning):
                    os.makedirs(Path)
                    print("Warning:CEPathCheck:Path '"+ Path +"' could not be found. It has now been created")

    def clearDir(this)->None:
        this.__ProPATH__.clear()

#Provide global variables for quick access
CEDirChc = CEDirCheck()
