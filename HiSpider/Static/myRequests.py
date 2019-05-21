# =============================================================================
# 1：请求（当前）
# 2：解析
# 3：保存
# =============================================================================

# =============================================================================
# 通过Requests抓取到静态页面的HTML代码
# 功能：GET/POST请求，会话，上传文件，SSL等认证，登录，代理，队列
# 发送前：
#   构造所有变量（URL（地址）,Headers（请求头）,Data（变量）,Proxies（代理）,File(上传文件)
#   是否需要Session，进行页面跳转,与队列互斥，而且要有后续操作，每一次操作返回一次html
#   是否需要Cookies维持登录状态
#   是否需证书验证
#   是否需要登陆，加密方式是哪种
#   是否需要提交不同数据（使用队列）
# =============================================================================

# 代理后面由单独的代理池取出
#self.proxies = {
#    "http":"http://10.10.1.10:3128",
#    "https":"http://10.10.1.10:1080"
#}
#若代理需要使用HTTP Basic Auth
#self.proxies = {
#    'http':'http://user:password@10.10.1.10:3128/',
#}

#r = requests.post('http://httpbin.org/post')
# r = requests.put('http://httpbin.org/put')            # 直接发送表单
# r = requests.delete('http://httpbin.org/delete')      # 删除email
# r = requests.head('http://httpbin.org/get')           # 少量流量获取表头
# r = requests.options('http://httpbin.org/get')        # 没找到是干嘛的
# 请求属性 
# r.url 
# r.status_code 状态码 
# r.text HTML<class 'str'> 
# r.cookies r.json() 解码<class 'dict'> 
# r.headers 响应头 
# -*- coding: utf-8 -*-
# r.history 请求历史


# 对于报头content-type没有说明编码方式的需要识别并转码
#r.encoding='utf-8'

#print(r.headers)
#html =r.read()

#code = chardet.detect(html)["encoding"]
#print(code)

#headers = {'User-Agent':'Mozilla/5.0(Macintosh;Intel Mac OS X 10_11_4) AppleWebKit/537.36(KHTML,like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
#x = requests.get(url, headers)
#x.encoding=code


#'Cookies':'__DAYU_PP=BfVyyUjqbj2ubAZEbzj672d46ed98311; _zap=ce094546-0948-4acb-aec1-afea25e8121e; d_c0="ANCga6ygbw2PTkMJrHiesM6hqLq8NcuDCGs=|1523609502"; z_c0=Mi4xNDBNY0JRQUFBQUFBMEtCcnJLQnZEUmNBQUFCaEFsVk5pNERhV3dCN0diQnJxc010NS0wR0NwdGZoVE5lOWpIWHdn|1525494411|03ea54795c87214e32ae86e3ffbed9b4ea9b1bea; __utma=51854390.546200048.1523609316.1523609316.1525494431.2; __utmz=51854390.1525494431.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100--|2=registration_date=20170603=1^3=entry_date=20170603=1; _xsrf=Er0dMSJD3Y4dqk4jw0IZ4dV5y8Cpo0bL; q_c1=8a9c555fb98448479de20c30c5195172|1535955855000|1521560122000; tgw_l7_route=156dfd931a77f9586c0da07030f2df36',
#url = "https://www.csdn.net/"
#headers = {'User-Agent':'Mozilla/5.0(Macintosh;Intel Mac OS X 10_11_4) AppleWebKit/537.36(KHTML,like Gecko) Chrome/52.0.2743.116 Safari/537.36',}
#data = {
#    "wd":"python",
#}

import requests
import urllib3
# 输入Request属性，输出HTML源码
class MyRequest(object):
    # def __init__(self, url='', headers='', data='', proxies='', timeout=1, username='', passwd='', IsUseSession=False, verify=False, filename=''):
    def __init__(self):
        # 基本属性
        self.url = ''
        self.headers = ''
        self.data = ''
        
        # 高级属性
        self.timeout = 0
        self.proxies = ''
        self.username = ''
        self.passwd = ''
        self.verify = ''
        self.filename = ''
        self.IsUseSession = False

    def progress(self):

        # 设置登陆加密方式
        #此外requests还提供其他认证方式，比如OAuth认证，不过需要安装oauth包，命令是pip install requests_oauthlib
        #from requests.oauthlib import Oauth1
        #self.auth = OAuth1('YOUR_APP_KEY','YOUR_APP_SECRET','USER_OAUTH_TOKEN','USER_OAUTH_TOKEN_SECRET')

        # 证书SSL忽略警告的方式来屏蔽
        urllib3.disable_warnings()

            
        #   是否需要Session，进行页面跳转,与队列互斥，而且要有后续操作，每一次操作返回一次html            
        #if self.IsUseSession:
            #s = requests.Session()
            #return s


        #   是否需要提交不同数据（使用队列）
        
    # 设置高级属性，长久生效
    def setOptions(self, proxies='', timeout=1, username='', passwd='', IsUseSession=False, verify=False, filename=''):
        self.timeout = timeout
        self.proxies = proxies
        
        self.username = username
        self.passwd = passwd
        
        self.verify = verify
        self.filename = filename
        self.IsUseSession = IsUseSession




    def gethtml(self, url, headers='', data=''):
        # 判断URL是否正确(这里现在没有用的，后面再添加验证)
#        try:
#            if self.url=='':
#                print("URL为空")
#                return False
#        except:
#            return False
        
        self.url = url
        self.headers = headers
        self.data = data
        try:
            self.progress()
        except:
            print("设置属性失败")
            return False 
        
        try:
            headers = {'User-Agent':'Mozilla/5.0(Macintosh;Intel Mac OS X 10_11_4) AppleWebKit/537.36(KHTML,like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
            r = requests.get(self.url, headers, data=self.data)

            print(r.url,r.status_code)
            return r.text
        except:
            print("请求错误")
            return False;

if __name__ == '__main__':
    mr = MyRequest()
    url = 'https://www.gameres.com/'



#####################################################################################################################
# 使用会话，维持了网页

#s.get('http://httpbin.org/cookies/set/number/123456789')
#r=s.get('http://httpbin.org/cookies')

#####################################################################################################################
# Request队列
# 独立的对象,意思就是每一次发送的都是独立的，比如cookies不保留
#from requests import Request,Session
#s = Session()
#req = Request('GET', url, data=data, headers=headers)
#prepped = s.prepare_request(req)

# do something with prepped.body
# do something with prepped.headers

#resp = s.send(prepped,stream=stream,verify=verify,proxies=proxies,cert=cert,timeout=timeout)
#####################################################################################################################



















