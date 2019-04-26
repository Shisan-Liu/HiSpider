# -*- coding: utf-8 -*-
# =============================================================================
# 思路
# 每个站点都会有“结构相同，内容不同”的页面
# 不管抓什么页面，最重要的是确定HTML结构
# 我们先找出高频词汇，再返回去看HTML，最后确定数据结构
# 高频词有可能是CSS属性、Txt文本、HTML结构

# 处理多张页面
# 如何找到结构相同，内容不同的页面的不同的地方？
# 抓取两张页面进行比对，确定固定不变的一些属性，重要内容就保存在两张页面中格式相同但是内容不同的部分

# 处理特定的版块：比如评论，我们只需要找到评论所在的DIV即可

# 抓表格，搜索引擎这种某个节点下的子节点特别多的
# 生成树，过滤，排序
# 树形结构来记录每一层节点子节点数目来判断，每一个节点保存完整的子节点信息，和子节点数目
# 根据每一层的节点数从大到小排序，重要数据不一定是第一个，但很大可能是前几个
# 过滤，首先过滤掉没有文字的部分

# 



# =============================================================================

# =============================================================================
# 进展
# 目前为止我只实现了根据文本的特征进行分类

# =============================================================================



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
# =============================================================================


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

class mainAnalyze(object):
    def __init__(self):
        self.html = ''
        # 过滤参数
        self.MinChildNum = 0                    # 节点中至少包含子节点数
        self.MaxEngishNum = 0                   # 节点中最多包含英文字符数目
        
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
    
    # 生成树并设置节点中的属性，并对树进行排序
    def start(self,html,minchildnum=5,maxengishnum=40):
        # 清理
        self.allnodelist = []
        self.diclist = []
        # 设置参数
        self.html = html
        self.MinChildNum = minchildnum
        self.MaxEngishNum = maxengishnum

        html = etree.HTML(self.html)
        result = etree.tostring(html)       
        html = result.decode('utf-8')                       # 补全html代码
        doc = pq(html)                                      # 转换为pq类型  
        parentnode = node(doc)                              # 把pq类型的html代码转换成node节点
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
        self.allnodelist.sort(reverse=True,key=lambda node:node.num)
        
        self.SpawnDic()
    
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
            for child in node.childlist:
                if(child.data.text()!=''):
                    dic = {i:child.data.text()}
                    self.diclist.append(dic)
    
