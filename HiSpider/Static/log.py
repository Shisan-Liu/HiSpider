# -*- coding: utf-8 -*-
import time,os
# =============================================================================
# 日志生成（其实可以合并到文件控制器中）
# =============================================================================


# 规范LOG信息（未完成）
# 每一个事件，执行前，执行中，执行后都要记录LOG事件
# 可以定义一个结构体在每个事件中进行设定，在记录时调用
# 后面还以在配置文件中进行修改
class loginfo(object):
    def __init__(self,defaultStartMessage, defaultEndMessage):
        self.Start=defaultStartMessage
        self.End=defaultEndMessage


class Log(object):

    def __init__(self):
        self.logHome = './log/'
        #检测文件夹是否创建
        if(os.path.exists(self.logHome)==False):
            os.mkdir(self.logHome)
        
        self.startlog = '加载Log模块。。。OK'
        self.write(self.startlog)
            
    def write(self,logstr):
        # 输入：信息
        # 输出：判断并生成一个log文件，写入时间戳+信息
        # 文件路径
        curtime =  time.localtime(time.time())
        filename = str(curtime.tm_year)+'-'+ str(curtime.tm_mon)+'-'+ str(curtime.tm_mday)+'.txt'
        logfilename = self.logHome+filename
            
        # 内容
        timehead = '['+str(curtime.tm_hour)+':'+str(curtime.tm_min)+':'+str(curtime.tm_sec)+']:'
        content = str(timehead) + str(logstr)
            
        # 写入文件
        with open(logfilename,'a',encoding='utf-8') as f:
            f.write(content)
            f.write('\n')  

            
         
if __name__=='__main__':
    testlog = Log()
    testlog.write('这是一条日志测试信息')