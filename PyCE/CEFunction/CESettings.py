#This document is translated from the C++ version of CESettings. CESettings is derived from PLSettings
import os
from PySide2.QtCore import *
from typing import *
from enum import *


class CESettings(QObject):
    """
    CommonEdit:Settings \n\n
    This class is used for CommonEdit to provide users with a convenient program Setting management mechanism \n
    When initializing a class, you can specify the actions that CESettings will take when it encounters invalid access keys.  \n
    By default (WhenBeyond.doException), an exception is raised to remind you that your program is wrong \n
    You can use setBeyondPolicy() to change this setting at any time, but it is not recommended.  \n
    Especially if you use CEMain for initialization, it is recommended not to change this setting again.
    """
    class SavePolicy(Enum):
        unknown = 0
        saveAtOnce = 1
        doNotSave = 2

    class WhenBeyond(Enum):
        unknown = 0
        doException = 1
        doRepairWithWarning = 2
        doRepairWithSlience = 3

    __SettingsPair__ = {}
    __gCESDir__:str
    __gBeyondPolicy__:WhenBeyond
    def __init__(this, beyondPolicy:WhenBeyond = WhenBeyond.doException, parent:QObject = None)->None:
        super().__init__(parent)
        this.setParent(parent)
        this.__gBeyondPolicy__ = beyondPolicy

    def setCESPath(this, CESPath:str)->None:
        """
        setCESPath(CESPath:str)->None \n\n
        Set the path of CES file \n
        If the CES file does not exist, a new CES file will be created in the specified path with the settings in the current program. \n
        So you should first use the setKVPair() function to load the default settings
        """
        this.__gCESDir__ = CESPath
        if (not os.path.exists(CESPath)) : 
            print("Warning:CESettings:Settings File '"+ CESPath +"'dose not exist.")
            this.save()

    def setKVPair(this, KVPair:Dict[str,str])->None:
        """
        setKVPair(KVPair:Dict[str,str])->None \n\n
        The setting key value pair of the setting program, that is, a dictionary whose keys and values are both str
        """
        this.__SettingsPair__ = KVPair

    def setBeyondPolicy(this, beyondPolicy:WhenBeyond)->None:
        """
        setBeyoundPolicy(beyoundPolicy:CESettings.WhenBeyond)->None \n\n
        The value is written in the same way as the initialization function. \n\n
        Did I remind you not to call this function alone?
        """
        this.__gBeyondPolicy__ = beyondPolicy

    def loadSettings(this)->bool:
        """
        loadSettings()->bool \n\n
        Call this function after setting the path of CES file\n
        When the CES file fails to load, it will return false.\n
        Generally speaking, it will not fail to load, unless the file is being occupied or deleted halfway. \n
        OR...\n
        You FORGOT to use setCESPath() to specify the location of the CES file in advance! \n
        """
        settingsFile = QFile()
        settingsFile.setFileName(this.__gCESDir__)
        settingsFile.open(QIODevice.ReadOnly | QIODevice.Text)
        if (not settingsFile.isOpen()) : 
            return False
        else:
            settingsFileText = QTextStream(settingsFile)
            settingsFileText.setCodec("UTF-8")
            while (True):
                if (settingsFileText.atEnd()) : break
                stSingleString=settingsFileText.readLine()
                if (stSingleString=="") : continue
                if (stSingleString[0] == "#" or stSingleString[0] == "\n") : continue
                this.__SettingsPair__[stSingleString.split("=")[0]] = stSingleString.split("=")[-1]        
            return True

    def valueOf(this, Key:str)->str:
        """
        valueOf(Key:str)->str \n
        Input key.Output value \n
        Don't make a wrong key, otherwise the Exception may come to your trouble\n
        """
        try:
            return this.__SettingsPair__[Key]
        except Exception:
            if (this.__gBeyondPolicy__ == this.WhenBeyond.doException):
                raise Exception("Exception:CESettings:Settings Key '"+ Key +"' could not be found in settings list.")
            elif (this.__gBeyondPolicy__ == this.WhenBeyond.doRepairWithSlience):
                this.__SettingsPair__[Key] = "None"
            elif (this.__gBeyondPolicy__ == this.WhenBeyond.doRepairWithWarning):
                this.__SettingsPair__[Key] = "None"
                print("Warning:CESettings:Settings Key '"+ Key +"' could not be found in settings list.It has now been initialized to 'None'")

    def setValue(this, Key:str, Value:str, savePolicy:SavePolicy = SavePolicy.saveAtOnce)->None:
        """
        setValue(Key:str,Value:str,savePolicy:CESettings.SavePolicy)\n
        Specify a new key and a new value and store them in the program settings cache\n
        By default, the cache will be written to the file immediately. \n
        You can specify CESettings.Savepolicy.doNotSave to manually write the file later\n
        Of course, if you use CEMain for program initialization, It will drive CESettings to save all settings before the program exits normally.\n
        Note that it means normal exit.
        """
        this.__SettingsPair__[Key] = Value
        if (savePolicy==this.SavePolicy.saveAtOnce):
            this.save()

    def getKeys(this)->List[str]:
        """
        getKeys()->List[str] \n
        Output a list of all keys in the program settings cache
        """
        return list(this.__SettingsPair__.keys())

    def save(this)->None:
        """
        save()->None\n
        Save program settings
        """
        SettingsText = ""
        for i in this.__SettingsPair__.keys():
            SettingsText += i + "=" + this.__SettingsPair__[i] + "\n"

        SettingsFile = QFile()
        SettingsFile.setFileName(this.__gCESDir__)
        SettingsFile.open(QIODevice.WriteOnly | QIODevice.Text)
        SettingsFile.write(SettingsText.encode("UTF-8")) 
        SettingsFile.close()

CESets = CESettings()