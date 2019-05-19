# -*- coding: utf-8 -*-

# =============================================================================
#  功能：抓取静态页面
#  输入url，确定，选择保存格式
#  抓取到本地（保存到temp文件夹）
#  解析设定，先调用Analyze中函数对目标网页进行分析，然后提供一系列选项给用户
#  选择是否要抓取更多（针对那种有很多页的，可以自动判断url中是否有page等数字，和页面内是否有按钮的href链接到相似url）
#  在result文件夹创建新的文件夹，用来保存数据
#  抓取每的一个页面调用save中的函数保存到刚才创建的文件夹中
# =============================================================================

# BUG:
# 缺少验证URL


import time,sys

from Static.myRequests import MyRequest as Request
from Static.urlrequest import urlrequest as uq
from Analyze.Analyze import Analyze

from Static.filecontroller import FileController as FC
from Static.module import Module

from PyQt5.QtWidgets import QApplication
from UI.MainUI import UserInterface


#'Cookies':'__DAYU_PP=BfVyyUjqbj2ubAZEbzj672d46ed98311; _zap=ce094546-0948-4acb-aec1-afea25e8121e; d_c0="ANCga6ygbw2PTkMJrHiesM6hqLq8NcuDCGs=|1523609502"; z_c0=Mi4xNDBNY0JRQUFBQUFBMEtCcnJLQnZEUmNBQUFCaEFsVk5pNERhV3dCN0diQnJxc010NS0wR0NwdGZoVE5lOWpIWHdn|1525494411|03ea54795c87214e32ae86e3ffbed9b4ea9b1bea; __utma=51854390.546200048.1523609316.1523609316.1525494431.2; __utmz=51854390.1525494431.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100--|2=registration_date=20170603=1^3=entry_date=20170603=1; _xsrf=Er0dMSJD3Y4dqk4jw0IZ4dV5y8Cpo0bL; q_c1=8a9c555fb98448479de20c30c5195172|1535955855000|1521560122000; tgw_l7_route=156dfd931a77f9586c0da07030f2df36',
#url = "https://www.csdn.net/"
#headers = {'User-Agent':'Mozilla/5.0(Macintosh;Intel Mac OS X 10_11_4) AppleWebKit/537.36(KHTML,like Gecko) Chrome/52.0.2743.116 Safari/537.36',}
#data = {
#    "wd":"python",
#}

# SpiderModel
class HiSpider:
    def __init__(self):

        # 本地模型名列表
        #self.LocalMoudle = []

        self.Request = Request()
        self.Analyze = Analyze()
        self.FC = FC()

        # 启动图形界面,并传入此Hispider实例引用
        # 用户对UI进行输入后，UI再对此类进行修改
        # 最后再调用UI中的函数更新页面

        app = QApplication(sys.argv)
        self.UI = UserInterface(self)
        self.MoudleCache = self.UI.pListView.getDiclist()           # 模型缓冲区

        sys.exit(app.exec_())


    def SendRequest(self,url,modulename,format):
        # 功能：由UI调用发送请求获取HTML
        # 输入：URL，模型名，保存格式
        urlq = uq()
        html = urlq.GetHtml(url)
        htmlcode = urlq.code
        #html = self.Request.gethtml(url)

        NewModule = Module(modulename)
        modulehome = NewModule.GetValue("ModuleHome")
        NewModule.SetUHF(url,html,format,htmlcode)

        self.UI.ShowModule(html)

        self.UI.pListView.addItem(NewModule)
        time.sleep(1)
        diclist = self.GetAnalyzeDiclist(html)

        self.UI.ShowDiclist(diclist,modulehome)

    def SaveDic(self,filename,diclist):
        self.FC.DicList_write(filename,diclist)


    def GetAnalyzeDiclist(self,html):

        self.Analyze.start(html)
        return self.Analyze.diclist

       
    def errorMessage(self,mes):
        return mes

if __name__ == '__main__':
    test = HiSpider()