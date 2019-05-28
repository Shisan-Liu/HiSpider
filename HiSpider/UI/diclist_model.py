
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

## Content数据框
#from Static.main import HiSpider  as HS
import sys

class DiclistWidget(QWidget):
    def __init__(self,dic,index):
        super().__init__()
        self.index = index

        self.ContentBox = QVBoxLayout()
        self.setLayout(self.ContentBox)

        if(dic!={}):
            # 标题
            ContentLabel = QLabel(dic["title"], self)
            self.ContentBox.addWidget(ContentLabel)
            # 内容
            for i,alabel in enumerate(dic["content"]):
                ContentLabel = QLabel(str(i)+" "+str(alabel), self)
                self.ContentBox.addWidget(ContentLabel)
            #
            self.HBox = QHBoxLayout()
            self.ContentBox.addLayout(self.HBox)
            # 勾选框
            self.checkbox = QCheckBox("选择",self)
            try:
                if(dic["select"]==False):
                    self.checkbox.setChecked(False)
                else:
                    self.checkbox.setChecked(True)
            except:
                print("没有select")
            self.HBox.addWidget(self.checkbox)
            #self.checkbox.stateChanged.connect(self.CheckChanged)
            # Title修改框
            self.keylab = QLabel("Key:",self)
            self.HBox.addWidget(self.keylab)
            self.ContentInput = QLineEdit(dic["title"], self)
            self.HBox.addWidget(self.ContentInput)
            self.ContentInput.setFixedWidth(300)
            self.HBox.addStretch(1)


    def GetIsSelect(self):
        return self.checkbox.isChecked()


    def GetTitle(self):
        return self.ContentInput.text()


if __name__ == '__main__':
    dic = {"title":"11","content":["1","2"]}
    app = QApplication(sys.argv)
    ex = DiclistWidget(dic)
    sys.exit(app.exec_())