
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *


#from Static.main import HiSpider  as HS
import sys

class DiclistWidget(QWidget):
    def __init__(self,lis):
        super().__init__()

        self.ContentBox = QVBoxLayout()
        self.setLayout(self.ContentBox)

        ## Content数据框
        ContentLabel = QLabel(str(lis["title"]), self)
        self.ContentBox.addWidget(ContentLabel)
        for i,alabel in enumerate(lis["content"]):
            ContentLabel = QLabel(str(i)+" "+str(alabel), self)
            self.ContentBox.addWidget(ContentLabel)

        self.HBox = QHBoxLayout()
        self.ContentBox.addLayout(self.HBox)

        self.ContentInput = QLineEdit('字典名', self)
        #self.ContentButton = QPushButton('', self)
        #self.ContentButton.clicked.connect()          # 链接到控制器函数发送请求

        
        self.HBox.addWidget(self.ContentInput)
        #self.HBox.addWidget(self.ContentButton)

if __name__ == '__main__':
    lis = ["11","12"]
    app = QApplication(sys.argv)
    ex = DiclistWidget(lis)
    sys.exit(app.exec_())