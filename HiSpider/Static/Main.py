# -*- coding: utf-8 -*-
import time,sys
from PyQt5.QtWidgets import QApplication

from Static.myRequests import MyRequest as Request
from Static.urlrequest import urlrequest as uq
from Analyze.Analyze import Analyze


from Model.model import Model
from Model.model_s import SimpleModel
from UI.MainUI import UserInterface

from Root.filecontroller import FileController

# 主控制器
class HiSpider(FileController):
    def __init__(self, *args, **kwargs):
        self.__confdic = {
                "confFilePath":'./Config/MainConf.json',
                "HistoryDicList":[]

        }
        self.Conf_load(self.__confdic)
        self.CurrentModule = Model("ModelName")
        # 请求
        self.Request = Request()
        self.urlquest = uq()

        # 解析
        self.Analyze = Analyze()
        
        return super().__init__(*args, **kwargs)

    def viewinit(self):
        # 初始化界面
        app = QApplication(sys.argv)
        self.UI = UserInterface(self)

        for sm in self.GetOldSimpleModelList():
            self.UI.AddModelHistory(sm)

        sys.exit(app.exec_())


    def GetOldSimpleModelList(self):
        modellist = []
        smlist = self.Get("HistoryDicList")
        for dic in smlist:
            sm = SimpleModel(dic["ModelName"],dic["url"])
            modellist.append(sm)
        return modellist


    def GetConfDic(self):
        return self.__confdic

    def Get(self,key):
        return self.__confdic[key]    

    def Conf_update(self):
        self.Conf_write(self.__confdic)

    def AddModelHistory(self,modelname,url):
        dic = {}
        for h in self.__confdic["HistoryDicList"]:
            if(h["ModelName"]==modelname):
                return 
        dic["ModelName"] = modelname
        dic["url"] = url
        self.__confdic["HistoryDicList"].append(dic)
        self.Conf_update()
    #def DeleteModelHistory(self,index)

    def SendRequest(self,url,modelname):
        self.CurrentModule = Model(modelname)
        html = self.urlquest.GetHtml(url)
        htmlcode = self.urlquest.code
        self.CurrentModule.Prepare(url,html,htmlcode)

        diclist = self.GetAnalyzeDiclist(html)

        self.CurrentModule.Set("diclist",diclist)
        # 显示
        sm = SimpleModel(modelname,url)
        self.UI.AddModelHistory(sm)
        self.UI.ShowModule(self.CurrentModule)
        # 添加抓取历史记录（URL，模型名）
        self.AddModelHistory(modelname,url)

    def GetAnalyzeDiclist(self,html):
        self.Analyze.start(html)
        return self.Analyze.diclist


if __name__ == '__main__':
    Hi = HiSpider()
    Hi.viewinit()