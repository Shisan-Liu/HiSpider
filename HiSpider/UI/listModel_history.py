#coding=utf-8


from PyQt5.QtCore import QAbstractListModel, Qt, QModelIndex, QVariant, QSize
from PyQt5.QtGui import QIcon, QFont

class ListModel(QAbstractListModel):
    def __init__(self):

        super().__init__()     
        self.ListItemData = []

    def data(self, index, role):
        if index.isValid() or (0 <= index.row() < len(self.ListItemData)):
            if role == Qt.DisplayRole:# 文本形式呈现数据
                return QVariant(self.ListItemData[index.row()].Get("ModelName")+"["+self.ListItemData[index.row()].Get("url")+"]")
                

            elif role == Qt.SizeHintRole:# 视图项目大小
                return QVariant(QSize(70, 40))
                
            elif role == Qt.TextAlignmentRole:# 文本对齐方式
                return QVariant(int(Qt.AlignHCenter|Qt.AlignVCenter))
                
            elif role == Qt.FontRole:# 字体设置
                font = QFont()
                font.setPixelSize(14)
                return QVariant(font)
                
        return QVariant()# 非上述情况，返回为空，记住这里是QVariant()
        

    def rowCount(self, parent = QModelIndex()):
        #返回行数，在这里就是数据列表的大小。
        return len(self.ListItemData)


    def addItem(self, itemData):
        #新增
        if itemData:
            self.beginInsertRows(QModelIndex(), len(self.ListItemData), len(self.ListItemData) + 1)
            self.ListItemData.append(itemData)
            self.endInsertRows()

    def deleteItem(self, index):
        #指定索引的数据从数据列表中删除
        del self.ListItemData[index]

    def getItem(self, index):
        #获得相应的项目数据
        if index > -1 and index < len(self.ListItemData):
            return self.ListItemData[index]
