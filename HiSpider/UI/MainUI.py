from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from UI.lstView_history import ListView
from UI.diclist_model import DiclistWidget
from Model.model import Model

import json
import sys

class UserInterface(QWidget):
    def __init__(self,HiSpidier):
        super().__init__()
        self.HiSpider = HiSpidier
        self.initUI()
        self.show()

    def initUI(self):
        self.setGeometry(0, 0, 1280, 720)
        self.setWindowTitle('HiSpider')
        # 水平主布局
        self.MainBox = QHBoxLayout()
        self.setLayout(self.MainBox)
        self.Left()
        self.Right()

    def Left(self):
        # 左侧纵向布局LeftBox
        self.LeftWidget = QWidget()
        self.LeftWidget.setFixedWidth(300)
        self.LeftWidget.setGeometry(0, 0, 400, 720)

        self.LeftBox = QVBoxLayout()
        self.LeftWidget.setLayout(self.LeftBox)

        self.MainBox.addWidget(self.LeftWidget)

        ## URL数据框
        self.URLLabel = QLabel('URL:', self)
        self.URLInput = QLineEdit('http://www.people.com.cn/', self)
        self.URLButton = QPushButton('Open', self)
        self.URLButton.clicked.connect(self.SubmitRequest)          # 链接到控制器函数发送请求

        self.URLBox = QHBoxLayout()
        self.URLBox.addWidget(self.URLLabel)
        self.URLBox.addWidget(self.URLInput)
        self.URLBox.addWidget(self.URLButton)

        self.LeftBox.addLayout(self.URLBox)

        # 输入ModelName
        self.ModelNameLabel = QLabel('模型名:', self)
        self.ModelNameInput = QLineEdit('ModelName', self)

        self.ModelNameBox = QHBoxLayout()
        self.ModelNameBox.addWidget(self.ModelNameLabel)
        self.ModelNameBox.addWidget(self.ModelNameInput)

        self.LeftBox.addLayout(self.ModelNameBox)

        # 导出文件
        self.ExportLabel = QLabel('导出文件名:', self)
        self.ExportInput = QLineEdit('content', self)
        self.exportBurrom = QPushButton("导出")
        self.exportBurrom.clicked.connect(self.Export)
        # 保存格式
        self.currentFormat = ".json"
        self.SaveFormat = QToolButton(self)
        #self.SaveFormat.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        #self.SaveFormat.setArrowType(Qt.DownArrow)             # 设置箭头方向
        self.SaveFormat.setText(self.currentFormat)                         # 设置图标和文字。
        self.SaveFormat.setAutoRaise(True)                      # 此属性保持是否启用自动升起
        self.SaveFormat.setPopupMode(QToolButton.InstantPopup)  #按下之后响应模式
        menu = QMenu(self)
        self.txtAct = QAction('.txt', self)
        self.jsonAct = QAction('.json', self)
        self.mysqlAct = QAction('.csv', self)
        menu.addAction(self.txtAct)
        menu.addAction(self.jsonAct)
        menu.addAction(self.mysqlAct)
        self.SaveFormat.setMenu(menu)
        self.txtAct.triggered.connect(self.SetFormat)
        self.jsonAct.triggered.connect(self.SetFormat)
        self.mysqlAct.triggered.connect(self.SetFormat)

        self.SaveFormatBox = QHBoxLayout()
        self.SaveFormatBox.addWidget(self.ExportLabel)
        self.SaveFormatBox.addWidget(self.ExportInput)
        self.SaveFormatBox.addWidget(self.SaveFormat)
        self.SaveFormatBox.addWidget(self.exportBurrom)

        self.LeftBox.addLayout(self.SaveFormatBox)        

        # Module缓存列表
        self.pListView = ListView(self.ShowModule) 
        self.pListView.setViewMode(QListView.ListMode)

        self.LeftBox.addWidget(self.pListView)


    def Right(self):
        # 右侧纵向布局RightBox
        self.RightBox = QVBoxLayout()
        self.MainBox.addLayout(self.RightBox)

        # tab内容标签
        self.tabWidget = QTabWidget()
        self.RightBox.addWidget(self.tabWidget)

        # 第一页
        self.HtmlTab = QWidget()
        self.Content1Box = QVBoxLayout()
        self.HtmlTab.setLayout(self.Content1Box)
        self.tabWidget.addTab(self.HtmlTab, "  HTML  ")
        # HTML显示窗口
        self.Content1 = QTextEdit(self)
        self.Content1Box.addWidget(self.Content1)



        # 第二页
        self.DiclistTab = QWidget()
        self.DiclistVBox = QVBoxLayout()
        self.DiclistTab.setLayout(self.DiclistVBox)
        self.tabWidget.addTab(self.DiclistTab, "  Diclist  ")
        self.widgetlist_dic = []    #diclist显示控件列表

        # 滚动条
        self.ScroWidget = QWidget()
        self.ScroWidgetVBox = QVBoxLayout()
        self.ScroWidget.setLayout(self.ScroWidgetVBox)

        self.DicScrollArea = QScrollArea()
        self.DicScrollArea.setWidget(self.ScroWidget)

        self.DiclistVBox.addWidget(self.DicScrollArea)
        self.DicScrollArea.setAutoFillBackground(True)
        self.DicScrollArea.setWidgetResizable(True)



        # 底部固定显示框
        self.ButtomWidget = QWidget()
        self.ButtomWidget.setFixedHeight(200)
        self.RightBox.addWidget(self.ButtomWidget)

        self.ButtomGLayout = QGridLayout()
        self.ButtomWidget.setLayout(self.ButtomGLayout)

        names = ["name"*25]

        for i in range(1,5):
            for j in range(1,5):
                if(i==1 and j==1):
                    exportBurrom = QPushButton("export")
                    exportBurrom.clicked.connect(self.Export)
                    self.ButtomGLayout.addWidget(exportBurrom,i,j,1,1)

        #self.ButtomGLayout.setSpacing(10)
        # 创建19个按钮

        #self.MainBox.addWidget(self.tabWidget)

        # 跑马灯
        #self.probar = QProgressBar(self)
        #self.probar.setOrientation(Qt.Horizontal)
        #self.probar.setFormat("%v")
        # ％p - 被完成的百分比取代
        # ％v - 被当前值替换


        #self.RightBox.addLayout(self.Content1Box)
        #self.RightBox.addWidget(self.probar)
        # MainBox


        #self.grid = QGridLayout()
        #self.grid.addWidget(self.LeftBox,0,0,1,1)
        #self.grid.addWidget(self.RightBox,0,1,1,1)


        #self.setLayout(self.grid)

        
    def SubmitRequest(self):
        # 提交URL获取HTML
        url = self.URLInput.text()
        modulename = self.ModelNameInput.text()
        self.HiSpider.SendRequest(url,modulename)

    def SaveDiclistEdit(self):
        # 更新UI界面中的设置到模型配置文件

        diclist = self.CurrentModule.Get("diclist")
        for w in self.widgetlist_dic:
            index = w.index
            isselect = w.GetIsSelect()
            title = w.GetTitle()

            diclist[index]["title"] = title
            diclist[index]["select"] = isselect
        self.CurrentModule.Conf_update()

    def Export(self):
        # 导出

        self.SaveDiclistEdit()
        filename = self.ExportInput.text() + self.currentFormat
        self.CurrentModule.OutPut(filename)

    def AddModelHistory(self,SimpleModel):
        #  list增加模型历史
        self.pListView.addItem(SimpleModel)

    def ShowModule(self,tModel):
        self.CurrentModule = tModel
        if(isinstance(tModel, Model)==False):
            self.CurrentModule = Model(tModel)
        else:
            self.CurrentModule = tModel
        # 显示HTML和Diclist

        html = self.CurrentModule.Get("html")
        
        self.Content1.setPlainText(html)# setPlainText纯文本，settext富文本
        # 清空显示diclist的控件
        if(len(self.widgetlist_dic)!=0):
            for i,w in enumerate(self.widgetlist_dic):
                w.deleteLater()
                del self.widgetlist_dic[i]

        diclist = self.CurrentModule.Get("diclist")
        print(diclist)
        if(diclist!=[]):
            for i,dic in enumerate(diclist):
                dw = DiclistWidget(dic,i)
                self.widgetlist_dic.append(dw)
                self.ScroWidgetVBox.addWidget(dw)


    def SetFormat(self):
        # 设置显示
        if self.sender() == self.txtAct:
            self.SaveFormat.setText(".txt")
            self.currentFormat = ".txt"
        elif self.sender() == self.jsonAct:
            self.SaveFormat.setText(".json")
            self.currentFormat = ".json"
        elif self.sender() == self.mysqlAct:
            self.SaveFormat.setText(".csv")
            self.currentFormat = ".csv"