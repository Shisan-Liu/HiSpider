# -*- coding: utf-8 -*-
# =============================================================================

# 目的：
# 找出高频词汇，自动化生成数据结构,高频词有可能是CSS属性、Txt文本、HTML结构
# 主要就是关注格式和内容，最终要得出一个组键值一一对应，值当然可能不止一个

# 相同类型信息多的：图片，表格，评论，搜索引擎
# 方法：
# 生成树，过滤，排序
# 树形结构来记录每一层节点子节点数目来判断，每一个节点保存完整的子节点信息，和子节点数目
# 根据每一层的节点数从大到小排序，重要数据不一定是第一个，但很大可能是前几个
# 过滤，首先过滤掉没有文字的部分
# 评论
# 视频网站，博客网站，知识网站，学习网站，新闻网站，评论中有大量的生活语言，后面可以用来进行机器学习分类算法的训练

# 结构相同，内容不同，相同类型数据少：博客
# 方法：
# 抓取两张页面进行比对，确定固定不变的一些属性，重要内容就保存在两张页面中格式相同但是内容不同的部分

# =============================================================================

from Static import MyRequests as Mr
from lxml import etree
from pyquery import PyQuery as pq


class node(object):
    def __init__(self,data):
        # 保存pyquery对象
        self.data = data
        # 记录该对象子节点个数
        self.num = len(data.children())

#'Cookies':'__DAYU_PP=BfVyyUjqbj2ubAZEbzj672d46ed98311; _zap=ce094546-0948-4acb-aec1-afea25e8121e; d_c0="ANCga6ygbw2PTkMJrHiesM6hqLq8NcuDCGs=|1523609502"; z_c0=Mi4xNDBNY0JRQUFBQUFBMEtCcnJLQnZEUmNBQUFCaEFsVk5pNERhV3dCN0diQnJxc010NS0wR0NwdGZoVE5lOWpIWHdn|1525494411|03ea54795c87214e32ae86e3ffbed9b4ea9b1bea; __utma=51854390.546200048.1523609316.1523609316.1525494431.2; __utmz=51854390.1525494431.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100--|2=registration_date=20170603=1^3=entry_date=20170603=1; _xsrf=Er0dMSJD3Y4dqk4jw0IZ4dV5y8Cpo0bL; q_c1=8a9c555fb98448479de20c30c5195172|1535955855000|1521560122000; tgw_l7_route=156dfd931a77f9586c0da07030f2df36',
url = 'https://www.cnblogs.com/luoye00/p/5223543.html'
headers = {
    'User-Agent':'Mozilla/5.0(Macintosh;Intel Mac OS X 10_11_4) AppleWebKit/537.36(KHTML,like Gecko) Chrome/52.0.2743.116 Safari/537.36',
}
#data = {
#    "wd":"python",
#}

# Requests获取HTML
myrq = Mr.MyRequest(url)
html = myrq.gethtml()

# 自动补全html代码
html =etree.HTML(html)
result = etree.tostring(html)
html = result.decode('utf-8')

# pyquery解析
doc = pq(html)
parentnode = node(doc)
parentlist = []
parentlist.append(parentnode)

# =============================================================================
# 生成"树"
# =============================================================================

treelist = []

# 多个父节点处理一个父节点
def SpawnTree(parentlist):
    newlist = []
    if(parentlist==[]):
        return
    else:
        for childnode in parentlist:            
            newlist = ChildNodeIntoTree(childnode)          
            SpawnTree(newlist)

# 输入一个有效的父节点，把子节点添加到treelist，返回添加的list
def ChildNodeIntoTree(parentnode):
    newlist = []
    # 如果该节点下面没有任何str，就不会添加到新节点，最后在SpawnTree中就return停止
    if(parentnode.data.text()!=''):
        # 将父节点的N个子节点保存到list，方便后面再对子节点进行计算子节点操作
        for child in parentnode.data.children():
            # 从html类型转换成Node类型
            pqchild = pq(child)
            childnode = node(pqchild)
            # 添加到节点列表
            newlist.append(childnode)
        # 添加到树节点
        treelist.append(newlist)
    return newlist


SpawnTree(parentlist)
#print(len(treelist))
numlist = []
for eachlist in treelist:
    num = 0
    for eachdiv in eachlist:
        num += eachdiv.num
    numlist.append(num)

maxnum = 0
maxindex = 0
for i,n in enumerate(numlist):
    if(n>maxnum):
        maxnum=n
        maxindex=i
#print(maxindex)

for item in treelist[maxindex]:
    print(item.data)

#i1 = treelist[0]
#print(len(i1),'\n',i1[0].data)
#print(i1[0].data)
#pqdoc = i1[1].data

#print(pqdoc.text())
#



#print(len(items))
#for i in items:
#    #<class 'lxml.etree._Element'>
#    pqi = pq(i)
#    #首先是否到达根部（文本）
#    if(isinstance(i,str)==False):
#        #获取子节点
#        pqitems = pqi.children()
#        print(len(pqitems))
#        for ic in pqitems:
#            pqic = pq(ic)

#        print(i)        
#        secitems = i.children()
#        print(len(secitems))


#
#items = doc('tr').items()
#
#for i in items:
#    print(i.text(),type(i))
#    ic = i.children()
#    print(1)
#    print(ic.text(),type(ic))
#    print(1)
#    icc = ic.children()
#    print(icc.text(),type(icc))
#    print(1)
#    iccc = icc.children()
#    if(iccc.text()==''):
#        print('tes')
#    print(iccc.text(),type(iccc))
#    print(2)
#    icccc = iccc.children()
#    print(icccc.text(),type(icccc))
#    break