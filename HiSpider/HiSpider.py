#conding=utf-8

from PyQt5.QtWidgets import *
from Static.Main import HiSpider  as HS
import sys

class Example(QWidget):
    def __init__(self):
        super().__init__()
        # Mine
        self.HS = HS()
        self.SaveFileFormat = '.txt'
        self.ModelName = ''

        # GUI
        self.initUI()
        self.show()

        

    def initUI(self):

        self.setGeometry(0, 0, 1280, 720)
        self.setWindowTitle('HiSpider')
        ## URLBOX
        self.URLLabel = QLabel('URL:', self)
        self.URLInput = QLineEdit('https://www.gameres.com/', self)
        self.URLButton = QPushButton('Open', self)
        self.URLButton.clicked.connect(self.Start)

        self.URLBox = QHBoxLayout()
        self.URLBox.addWidget(self.URLLabel)
        self.URLBox.addWidget(self.URLInput)
        self.URLBox.addWidget(self.URLButton)

        # Content1Box
        self.Content1 = QTextEdit(self)
        self.Content1.setGeometry(20, 20, 300, 270)

        self.Content1Box = QHBoxLayout()
        self.Content1Box.addWidget(self.Content1)


        # ModelName
        self.ModelNameLabel = QLabel('模型名:', self)
        self.ModelNameInput = QLineEdit('ModelName', self)



        self.ModelNameBox = QHBoxLayout()
        self.ModelNameBox.addWidget(self.ModelNameLabel)
        self.ModelNameBox.addWidget(self.ModelNameInput)

        # 保存路径

        # SaveFormat
        self.SaveFormatLabel = QLabel('保存格式:', self)
        self.SaveFormat = QToolButton(self)
        #self.SaveFormat.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        
        #self.SaveFormat.setArrowType(Qt.DownArrow)# 设置箭头方向
       
        self.SaveFormat.setText(self.SaveFileFormat) # 设置图标和文字。
        
        self.SaveFormat.setAutoRaise(True)# 此属性保持是否启用自动升起

        self.SaveFormat.setPopupMode(QToolButton.InstantPopup)#按下之后响应模式

        menu = QMenu(self)
        self.txtAct = QAction('TXT', self)
        self.jsonAct = QAction('JSON', self)
        self.mysqlAct = QAction('Mysql', self)
        menu.addAction(self.txtAct)
        menu.addAction(self.jsonAct)
        menu.addAction(self.mysqlAct)
        self.SaveFormat.setMenu(menu)
        self.txtAct.triggered.connect(self.SetSaveFormat)
        self.jsonAct.triggered.connect(self.SetSaveFormat)
        self.mysqlAct.triggered.connect(self.SetSaveFormat)

        self.SaveFormatBox = QHBoxLayout()
        self.SaveFormatBox.addWidget(self.SaveFormatLabel)
        self.SaveFormatBox.addWidget(self.SaveFormat)

        ## ConfigBox
        self.ConfigBox = QVBoxLayout()
        self.ConfigBox.addLayout(self.ModelNameBox)
        self.ConfigBox.addLayout(self.SaveFormatBox)

        

        # LeftBox
        self.LeftBox = QVBoxLayout()
        self.LeftBox.addLayout(self.URLBox)
        self.LeftBox.addLayout(self.ConfigBox)
        

        #RightBox
        self.RightBox = QVBoxLayout()
        self.RightBox.addLayout(self.Content1Box)

        # MainBox
        self.MainBox = QHBoxLayout()
        self.MainBox.addLayout(self.LeftBox)
        self.MainBox.addLayout(self.RightBox)

        # 把垂直布局盒子设置成主要的布局
        self.setLayout(self.MainBox)

      
        
    def Start(self):
        targeturl = self.URLInput.text()
        if(self.ModelName==''):
            self.ModelName = targeturl

        # 设置输入内容
        self.HS.seturl(targeturl,self.ModelName,self.SaveFileFormat)
        # 设置显示
        content = self.HS.Html
        self.Content1.setText(content)

    def SetSaveFormat(self):
        if self.sender() == self.txtAct:
            self.SaveFileFormat = '.txt'
            self.SaveFormat.setText(self.SaveFileFormat)
        elif self.sender() == self.jsonAct:
            self.SaveFileFormat = '.json'
            self.SaveFormat.setText(self.SaveFileFormat)
        elif self.sender() == self.mysqlAct:
            self.SaveFileFormat = '.mysql'
            self.SaveFormat.setText(self.SaveFileFormat)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())