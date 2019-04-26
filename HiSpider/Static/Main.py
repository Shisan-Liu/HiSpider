# -*- coding: utf-8 -*-

# =============================================================================
#  功能：抓取静态页面
#  输入url，确定，选择保存格式
#  抓取到本地（保存到temp文件夹）
#  解析设定，先调用Analyze中函数对目标网页进行分析，然后提供一系列选项给用户
#  选择是否要抓取更多（针对那种有很多页的，可以自动判断url中是否有page等数字，和页面内是否有按钮的href链接到相似url）
#  在result文件夹创建新的文件夹，用来保存数据
#  抓取每的一个页面调用save中的函数保存到刚才创建的文件夹中
# =============================================================================


import time

import myRequests as Mr

import analyze,save

#'Cookies':'__DAYU_PP=BfVyyUjqbj2ubAZEbzj672d46ed98311; _zap=ce094546-0948-4acb-aec1-afea25e8121e; d_c0="ANCga6ygbw2PTkMJrHiesM6hqLq8NcuDCGs=|1523609502"; z_c0=Mi4xNDBNY0JRQUFBQUFBMEtCcnJLQnZEUmNBQUFCaEFsVk5pNERhV3dCN0diQnJxc010NS0wR0NwdGZoVE5lOWpIWHdn|1525494411|03ea54795c87214e32ae86e3ffbed9b4ea9b1bea; __utma=51854390.546200048.1523609316.1523609316.1525494431.2; __utmz=51854390.1525494431.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100--|2=registration_date=20170603=1^3=entry_date=20170603=1; _xsrf=Er0dMSJD3Y4dqk4jw0IZ4dV5y8Cpo0bL; q_c1=8a9c555fb98448479de20c30c5195172|1535955855000|1521560122000; tgw_l7_route=156dfd931a77f9586c0da07030f2df36',
url = 'https://www.csdn.net/'
headers = {
    'User-Agent':'Mozilla/5.0(Macintosh;Intel Mac OS X 10_11_4) AppleWebKit/537.36(KHTML,like Gecko) Chrome/52.0.2743.116 Safari/537.36',
}
#data = {
#    "wd":"python",
#}

# 获取HTML
myrq = Mr.MyRequest()
html = myrq.gethtml(url)
if(html):
    # 分析HTML
    ana = analyze.mainAnalyze()
    ana.start(html)
    diclist = ana.diclist
    print(diclist)
    
    
    # 保存器
    foldername = 'baidunews'
    curtime =  time.localtime(time.time())   
    filename = str(curtime.tm_year)+'-'+ str(curtime.tm_mon)+'-'+ str(curtime.tm_mday)
    filetype = '.txt'
    saver = save.Save()
    saver.write(foldername,filename,diclist,filetype)


