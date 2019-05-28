
from Root.filecontroller import FileController

class SimpleModel(FileController):
    def __init__(self,*args, **kwargs):
        self.__confdic = {
                "ModelName":args[0],
                "confFilePath":"./content/"+args[0]+"/Conf/Conf.json",
                "url":args[1]
        }
        return super().__init__()
    def Get(self,key):
        return self.__confdic[key]    