#conding=utf-8

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from UI.ListView import ListView
from UI.DiclistModule import DiclistWidget
#from Static.main import HiSpider  as HS
import sys

class UserInterface(QWidget):
    def __init__(self,HiSpidier):
        super().__init__()
        # 控制器
        self.HiSpider = HiSpidier
        # GUI
        self.initUI()
        self.show()

        self.ModuleIndex = 0


    def initUI(self):

        self.setGeometry(0, 0, 1280, 720)
        self.setWindowTitle('HiSpider')

        # 水平主布局
        self.MainBox = QHBoxLayout()
        self.setLayout(self.MainBox)

        # 左侧纵向布局LeftBox
        #######################################################################
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

        # 保存格式选择MENU
        self.SaveFormatLabel = QLabel('保存格式:', self)
        self.SaveFormat = QToolButton(self)
        #self.SaveFormat.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        #self.SaveFormat.setArrowType(Qt.DownArrow)             # 设置箭头方向
        self.SaveFormat.setText(".txt")                         # 设置图标和文字。
        self.SaveFormat.setAutoRaise(True)                      # 此属性保持是否启用自动升起
        self.SaveFormat.setPopupMode(QToolButton.InstantPopup)  #按下之后响应模式
        menu = QMenu(self)
        self.txtAct = QAction('TXT', self)
        self.jsonAct = QAction('JSON', self)
        self.mysqlAct = QAction('Mysql', self)
        menu.addAction(self.txtAct)
        menu.addAction(self.jsonAct)
        menu.addAction(self.mysqlAct)
        self.SaveFormat.setMenu(menu)
        self.txtAct.triggered.connect(self.SetFormat)
        self.jsonAct.triggered.connect(self.SetFormat)
        self.mysqlAct.triggered.connect(self.SetFormat)

        self.SaveFormatBox = QHBoxLayout()
        self.SaveFormatBox.addWidget(self.SaveFormatLabel)
        self.SaveFormatBox.addWidget(self.SaveFormat)

        self.LeftBox.addLayout(self.SaveFormatBox)        

        # Module缓存列表
        self.pListView = ListView(self.ShowModule) 
        self.pListView.setViewMode(QListView.ListMode)

        self.LeftBox.addWidget(self.pListView)


        #self.MainBox.addLayout(self.LeftWidget)



        # 右侧纵向布局RightBox
        #######################################################################
        self.RightBox = QVBoxLayout()

        self.MainBox.addLayout(self.RightBox)
        # tab内容标签
        self.tabWidget = QTabWidget()
        self.RightBox.addWidget(self.tabWidget)
        #self.tabWidget.setObjectName("tabWidget")
        # 第一页
        self.HtmlTab = QWidget()
        #self.tab.setObjectName("tab1")
        # HTML显示窗口
        self.Content1 = QTextEdit(self)
        #self.Content1.setGeometry(20, 20, 300, 270)
        self.Content1Box = QVBoxLayout()
        self.Content1Box.addWidget(self.Content1)
        self.HtmlTab.setLayout(self.Content1Box)
        self.tabWidget.addTab(self.HtmlTab, "  HTML  ")

        # 第二页
        self.DiclistTab = QWidget()
        self.DiclistVBox = QVBoxLayout()
        self.DiclistTab.setLayout(self.DiclistVBox)
        #self.tab2.setObjectName("tab2")

        self.ScroWidget = QWidget()

        self.ScroWidgetVBox = QVBoxLayout()
        self.ScroWidget.setLayout(self.ScroWidgetVBox)

        self.DicScrollArea = QScrollArea()
        self.DicScrollArea.setWidget(self.ScroWidget)

        self.DiclistVBox.addWidget(self.DicScrollArea)
        self.DicScrollArea.setAutoFillBackground(True)
        self.DicScrollArea.setWidgetResizable(True)

        self.tabWidget.addTab(self.DiclistTab, "  Diclist  ")

        # 底部固定显示框
        self.ButtomWidget = QWidget()
        self.ButtomWidget.setFixedHeight(300)
        self.RightBox.addWidget(self.ButtomWidget)


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
        # 把垂直布局盒子设置成主要的布局

        #self.setLayout(self.grid)



    def SubmitRequest(self):
        # 提交URL获取HTML
        url = self.URLInput.text()
        modulename = self.ModelNameInput.text()
        format = self.GetFormat()
        self.HiSpider.SendRequest(url,modulename,format)

    def ShowDiclist(self,diclist):

        #self.ScroWidgetVBox.removeWidget()
        for i in diclist:
            dw = DiclistWidget(i)


            self.ScroWidgetVBox.addWidget(dw)


    def ShowModule(self,html):

        #self.probar.setMinimum(0)
        #self.probar.setMaximum(0)
        self.Content1.setPlainText(html)            # setPlainText直接设置成纯文本，settext会渲染html富文本


    def SetFormat(self):
        if self.sender() == self.txtAct:
            self.SaveFormat.setText(self.SaveFileFormat)
        elif self.sender() == self.jsonAct:
            self.SaveFormat.setText(self.SaveFileFormat)
        elif self.sender() == self.mysqlAct:
            self.SaveFormat.setText(self.SaveFileFormat)


    def GetFormat(self):
        if self.sender() == self.txtAct:
            return '.txt'
        elif self.sender() == self.jsonAct:
            return '.json'
        elif self.sender() == self.mysqlAct:
            return '.mysql'



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = UserInterface()
    sys.exit(app.exec_())