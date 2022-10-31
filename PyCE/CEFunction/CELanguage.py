#This File contains the CELanguage System translated from C++ Version
#It can also be said to be the improved SPLanguage System(Python)
from enum import *
from PyCE.CEFunction.CESettings import *
import os

class CELanguageName(Enum):
    unknown = "unknown"
    zh_CN = "zh_CN"
    en_US = "en_US"
    zh_TW = "zh_TW"

CEInverseEnumLangName = {
        "unknown":CELanguageName.unknown,
        "zh_CN":CELanguageName.zh_CN,
        "en_US":CELanguageName.en_US,
        "zh_TW":CELanguageName.zh_TW
    }
"""
CEInverseEnumLangName\n
DO NOT USE IT BY YOURSELF,this dictionary can only be used by CE itself.
"""

class CELanguage:
    """
    CommonEdit:Language\n
    ===\n
    You can use a global CELanguage class that has been created, and its name is CELangSys\n
    ===\n
    This class is used by CommonEdit to provide users with a multilingual translation mechanism\n
    The file it reads is a text file with the suffix '.celang' in its name.\n 
    Each line in the text file is divided into two parts with colons. \n
    The first part is the internal code, and the second part is the translated text.\n
    Use the enumeration class CELanguageName to set the language, \n
    or use the static method fromStr() provided by CELanguage to automatically complete the conversion from language name to enumeration class
    """
    __LangName__ = CELanguageName.unknown
    __DirPath__ = ""
    __InDevelop = False
    __TransDict__ = {}
    def __init__(this,LanguageName:CELanguageName = CELanguageName.unknown)->None:
        this.__LangName__ = LanguageName

    def setName(this, LanguageName:CELanguageName)->None:
        """
        setName(LanguageName:CELanguageName)->None\n
        Use the enumeration class CELanguageName to set the language, \n
        or use the static method fromStr() provided by CELanguage to automatically complete the conversion from language name to enumeration class
        """
        if ((LanguageName in CELanguageName) and (not LanguageName==CELanguageName.unknown)):
            this.__LangName__ = LanguageName        
        else:
            this.__LangName__ = CELanguageName.zh_CN
            print("Error:CESettings:The specified target '"+ LanguageName.value +"' is not in the CELanguageName enumeration class. The language is now set to zh_CN")
            CESets.setValue("Language","zh_CN")

    @staticmethod
    def fromStr(LanguageName:str)->CELanguageName:
        """
        static : fromStr(LanguageName:str)->CELanguageName\n
        Type the string of the language name and return the CELanguageName enumeration class object. \n
        If the language name is not in the enumeration class, CELanguageName.unknown will be returned
        """
        try:
            return CEInverseEnumLangName[LanguageName]
        except Exception:
            return CELanguageName.unknown

    def setPath(this, DirPath:str)->None:
        """
        setPath(DirPath:str)->None\n
        Set the path of the celang file.
        """
        this.__DirPath__ = DirPath

    def load(this)->bool:
        """
        load()->bool
        Read the celang file.\n
        It returns True when reading is successful and False when reading fails. \n
        There are two possible reasons for failure. The first is that the file does not exist and the second is that the file is occupied. \n
        When you fail to set the language name effectively, that is, the language name enumeration value is still CELanguageName.unknown, using this function will cause exceptions
        """
        if (this.__LangName__ == CELanguageName.unknown) :
            raise Exception("Exception:CELanguage:The file could not be loaded because no effective language type was specified")
        TargetFileName = this.__DirPath__ + "\\" + this.__LangName__.value +".celang"
        if (os.path.exists(TargetFileName)) :
            if (os.access(TargetFileName,os.R_OK)):
                TargetFile = open(TargetFileName,"r",encoding="utf-8")
                for Line in TargetFile.readlines():
                    if (Line=="") : continue
                    if (Line[-1]!="\n"): Line += "\n"
                    if ((Line[0]!="#") and (Line[0]!="\n") and (Line[0]!="")): 
                        if ":" not in Line : 
                            print("Warning:CELanguage:The separator ':' was not checked on line ' " + Line + " ' in the file:" + TargetFileName)
                            continue
                        this.__TransDict__[Line.split(":")[0]]=Line.split(":")[1][0:-1]
                TargetFile.close()
                return True
            else:
                print("Error:CELanguage:The specified file '"+ TargetFileName +"' is unreadable")
                return False
        else:
            print("Error:CELanguage:The specified file '"+ TargetFileName +"' could not be found")
            return False

    def returnValueOf(this,Key:str)->str:
        """
        returnValueOf(Key:str)->str\n
        Input key.Output value\n
        If the function fails to find the input key from the built-in dictionary, \n
        an error message will be output on the console and the key will be returned intact\n
        ===\n
        If you are using the CELangSys, you can use a global function msg() instead of this member function to use translation\n
        ===
        """
        try:
            return this.__TransDict__[Key]
        except Exception:
            print("Error:CELanguage:The translated text corresponding to the key'" + Key + "' could not be found")
            if (this.__InDevelop):
                this.__TransDict__[Key] = ""
            return Key

    def setDevelop(this,InDevelop:bool)->None:
        """
        setDevelop(InDevelop:bool)->None\n
        Set the language to be in development mode.\n
        In development mode, you can use the function "develop" to output a file contains keys that haven`t had translated\n
        """
        this.__InDevelop = InDevelop

    def develop(this)->None:
        """
        develop()->None\n
        Output the contents of the built-in dictionary\n
        This function is called internally by CEMain and output at the end of the program.\n
        All you need to do is call another function setDevelop with the parameter True
        """
        TargetFileName = this.__DirPath__ + "\\" + this.__LangName__.value +"_DEV.celang"

        TargetFile = open(TargetFileName,"w+",encoding="utf-8")
        for Key in this.__TransDict__.keys():
            TargetFile.write(Key + ":" + this.__TransDict__[Key] + "\n")
        TargetFile.close()


        

#Provide a global variable named CELangSys and a global function pointer named msg to quickly access the celanguage system.
#With these two variables, the SPLanguage System can also be quickly migrated to the CELanguage System
CELangSys = CELanguage()
msg = CELangSys.returnValueOf
