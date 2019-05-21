
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *


#from Static.main import HiSpider  as HS
import sys

class DiclistWidget(QWidget):
    def __init__(self,lis):
        super().__init__()

        self.isSelect = False

        self.ContentBox = QVBoxLayout()
        self.setLayout(self.ContentBox)

        ## Content数据框
        self.key = str(lis["title"])
        self.vallist = lis["content"]
        
        ContentLabel = QLabel(self.key, self)
        self.ContentBox.addWidget(ContentLabel)
        for i,alabel in enumerate(self.vallist):
            ContentLabel = QLabel(str(i)+" "+str(alabel), self)
            self.ContentBox.addWidget(ContentLabel)

        self.HBox = QHBoxLayout()
        self.ContentBox.addLayout(self.HBox)

        self.checkbox = QCheckBox("选择",self)
        self.HBox.addWidget(self.checkbox)
        self.checkbox.stateChanged.connect(self.CheckChanged)

        self.keylab = QLabel("Key:",self)
        self.HBox.addWidget(self.keylab)

        self.ContentInput = QLineEdit(self.key, self)
        self.HBox.addWidget(self.ContentInput)
        self.ContentInput.setFixedWidth(300)
        #spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.HBox.addStretch(1)

    def CheckChanged(self):
        if self.checkbox.isChecked():
            self.isSelect = True

        else:
            self.isSelect = False




if __name__ == '__main__':
    lis = {"title":"11","content":["1","2"]}
    app = QApplication(sys.argv)
    ex = DiclistWidget(lis)
    sys.exit(app.exec_())