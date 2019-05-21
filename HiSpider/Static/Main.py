# -*- coding: utf-8 -*-
import time,sys
from Static.myRequests import MyRequest as Request
from Static.urlrequest import urlrequest as uq
from Analyze.Analyze import Analyze
from Static.filecontroller import FileController as FC
from Static.module import Module
from PyQt5.QtWidgets import QApplication
from UI.MainUI import UserInterface

# 主控制器
class HiSpider:
    def __init__(self):
        # 请求
        self.Request = Request()
        self.urlquest = uq()

        # 解析
        self.Analyze = Analyze()

        # 文件控制器
        self.FC = FC()

        # 初始化界面
        app = QApplication(sys.argv)
        self.UI = UserInterface(self)

        # 获得模型列表的引用
        self.MoudleCache = self.UI.pListView.getDiclist()

        sys.exit(app.exec_())


    def SendRequest(self,url,modulename):
        # UI调用，传入url和模型名，获得并显示html和diclist
        # 实例化新Module
        NewModule = Module(modulename)
        html = self.urlquest.GetHtml(url)
        htmlcode = self.urlquest.code
        NewModule.SetUHF(url,html,htmlcode)
        diclist = self.GetAnalyzeDiclist(html)
        NewModule.SetValue("diclist",diclist)

        # 显示
        self.UI.pListView.addItem(NewModule)
        self.UI.ShowModule(NewModule)

    def GetAnalyzeDiclist(self,html):
        # 解析函数，现在只有一种解析方式，后面再增加
        self.Analyze.start(html)
        return self.Analyze.diclist

if __name__ == '__main__':
    Hi = HiSpider()
# 问题
# 缺少验证类型
