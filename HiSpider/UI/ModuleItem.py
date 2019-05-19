#coding=utf-8


from PyQt5.QtCore import QAbstractListModel, Qt, QModelIndex, QVariant, QSize
from PyQt5.QtGui import QIcon, QFont

class ListModel(QAbstractListModel):

    def __init__(self):

        super().__init__()     
        self.ListItemData = []

        #self.Data_init()

    def data(self, index, role):
        if index.isValid() or (0 <= index.row() < len(self.ListItemData)):
            if role == Qt.DisplayRole:
                return QVariant(self.ListItemData[index.row()].GetValue("MoudleName")+"["+self.ListItemData[index.row()].GetValue("url")+"]")
                # 文本形式呈现数据

            elif role == Qt.SizeHintRole:
                return QVariant(QSize(70, 40))
                # 视图项目大小
            elif role == Qt.TextAlignmentRole:
                return QVariant(int(Qt.AlignHCenter|Qt.AlignVCenter))
                # 文本对齐方式
            elif role == Qt.FontRole:
                font = QFont()
                font.setPixelSize(14)
                return QVariant(font)
                # 字体设置
        return QVariant()
        # 非上述情况，返回为空，记住这里是QVariant()

    def rowCount(self, parent = QModelIndex()):
        #返回行数，在这里就是数据列表的大小。
        return len(self.ListItemData)


    def addItem(self, itemData):
        #新增的操作实现
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
