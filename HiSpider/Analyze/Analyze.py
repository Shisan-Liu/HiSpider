# -*- coding:utf-8 -*- 
# =============================================================================
# 进展
# 目前为止我只实现了根据文本的特征进行分类

# =============================================================================
# 文章页面找文字最多的div和h
# 首页根据h找兄弟节点，找h的父节点的兄弟节点，找ul，找tr


# =============================================================================
# 调用方法
# ana = analyze.mainAnalyze()
# ana.start(html)
# diclist = ana.diclist
# 说明：实例化analyze对象之后，以后每次只用调用start函数传入参数即可
# =============================================================================

# =============================================================================
# BUG：
# 1-如果文本中包含代码，将会被错误的过滤掉
# 2-还没有找到合适的去除重复的方法
# 3-还无法确定字典的键
# 4-一个字典里面的字段也无法确定
# 一个div中的文字，有\n，需要再分割
# =============================================================================
from Static.myRequests import MyRequest as Request
from Static.urlrequest import urlrequest as uq

from lxml import etree
from pyquery import PyQuery as pq

class node(object):
    def __init__(self,data):
        self.childlist = []                     # list类型，保存所有直接子节点
        self.data = data                        # 节点本身的内容,pq类型
        self.num = 0                            # 子层级数目
        self.chinese = 0
        self.engish = 0
        self.rate = 0        
    def SetNum(self):
        self.num = len(self.childlist)          #用子列表长度设置子层级长度



class Analyze(object):
    def __init__(self):
        self.html = ''
        self.allnodelist = []                   # 所有节点
        self.diclist = []                       # 最终的字典列表
        
    # 递归对每一个节点生成子列表
    def SpawnTree(self,parentlist):
        # 判断是否有子节点
        if(parentlist==[]):
            return
        else:
            # 遍历该节点的所有子节点，生成子节点的子节点列表，对返回的每一个子节点再次执行此操作
            for childnode in parentlist:
                self.SpawnTree(self.ChildNodeIntoTree(childnode))
    # 输入节点，把子节点添加到该节点的子节点列表中，再把该节点添加到列表中，返回该节点的子节点列表
    def ChildNodeIntoTree(self,parentnode):
        if(parentnode.data.text()!=''):                     # 节点必须有文本
            for child in parentnode.data.children():          
                parentnode.childlist.append(node(pq(child)))# 子节点添加到子节点列表中
            self.allnodelist.append(parentnode)             # 该节点添加到列表中
        return parentnode.childlist
    
    def prepare(self,html):
        # 清理
        self.allnodelist = []
        self.diclist = []

        html = etree.HTML(html)
        result = etree.tostring(html)       
        html = result.decode('utf-8')                       # 补全html代码
        # 设置参数
        self.html = html

    # 生成树并设置节点中的属性，并对树进行排序
    def start(self,html):
        self.prepare(html)


        self.doc = pq(self.html)                                 # 转换为pq类型  
        parentnode = node(self.doc)                              # 把pq类型的html代码转换成node节点
        self.parentlist = []
        self.parentlist.append(parentnode)                  # 节点添加到列表
        # 生成节点树
        self.SpawnTree(self.parentlist)                     
        # 设置节点属性
        for eachnode in self.allnodelist:
            eachnode.SetNum()                               # 设置子节点数量
            for c in eachnode.data.text():                  # 统计中英文的字数和比例
                code = ord(c)
                if(code >= 97 and code <= 122):eachnode.engish += 1
                elif(code>=19968):eachnode.chinese += 1
            if(eachnode.engish!=0):
                eachnode.rate = eachnode.chinese/eachnode.engish
        self.allnodelist.sort(reverse=True,key=lambda node:node.num)    #从大到小排序
        self.diclist = self.FindHBorther()
        #self.SpawnDic()
    
    # 根据子节点数过滤
    def getNodeListNumLessX(self,nodelist,x):
        list = []
        for child in nodelist:
            if(child.num>=x):
                list.append(child)
        return list
    
    # 根据英文字符数过滤
    def getNodeListEngishLessX(self,nodelist,x):
        list = []
        for child in nodelist:
            if(child.engish<=x):
                list.append(child)
        return list
    
    # 去重
    # 去掉子节点数量最大和最小(是否需要去掉还要看是否重复)
    #del self.chinesenodelist[len(self.chinesenodelist)-1]
    #del self.chinesenodelist[0]    
    
    # 生成字典列表
    def SpawnDic(self):
        
        # 过滤掉子节点小于一定数目的
        CurrentNodeList = self.getNodeListNumLessX(self.allnodelist,5)
        
        # 检查文本中英文数量，如果还有英文说明代码不是纯的HTML（BUG-但是也有可能是代码）
        CurrentNodeList = self.getNodeListEngishLessX(CurrentNodeList,50)
        
        # 生成字典
        for i,node in enumerate(CurrentNodeList):
            childlis = []
            for child in node.childlist:
                if(child.data.text()!=''):
                    dic = {i:child.data.text()}
                    childlis.append(dic)
            self.diclist.append(childlis)

    #h的兄弟节点
    def  FindHBorther(self):
        # 'http://www.people.com.cn/'
        hlist = []
        h2 = self.doc("h3")
        #print(h2)
        for i,h in enumerate(h2):
            hdic = {}
            pqh = pq(h)
            pqhtxt = pqh.text()
            print(pqhtxt)
            hdic["title"] = pqhtxt
            content = []
            # h2的兄弟节点
            hbor = pqh.siblings()
            for bor in hbor:
                achbor = pq(bor)
                txt = achbor.text()
                lines = txt.split("\n")
                for line in lines:
                    content.append(line)
            hdic["content"] = content
            hlist.append(hdic)
        return hlist

    def FindUL(self):
        # http://www.aweb.com.cn/
        # http://bbs.tianya.cn/list-free-1.shtml
        uls = []
        ul = self.doc("ul")
        print(ul)
        for i,u in enumerate(ul):
            children_list = []
            pqu = pq(u)
            lis = pqu.children()
            for li in lis:
                pqli = pq(li)
                txt = pqli.text()
                children_list.append(txt)
            uls.append(children_list)
            print(children_list)
                

if __name__=="__main__":
    url = 'http://bbs.tianya.cn/list-free-1.shtml'

    urlq = uq()
    html = urlq.GetHtml(url)

    ana = Analyze()
    ana.start(html)
    ana.FindUL()

'''
doc = pq(html)

htmlTitle = doc("title").text()
print(htmlTitle)

ullist = doc('table')
for i in ullist:
    pqul = pq(i)
    print(pqul)

divlist = doc('div')
for item in divlist:
    eachdiv = pq(item)
    #print()
    #print(eachdiv.attr("class"),eachdiv.attr("id"))
    print(eachdiv)
'''



