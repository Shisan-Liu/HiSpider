# -*- coding: utf-8 -*-
import time,os
# =============================================================================
# 按照日期在log文件夹下创建log文件记录操作
# =============================================================================
# =============================================================================
# 输入：信息
# 输出：判断并生成一个log文件，写入时间戳+信息/错误信息
# =============================================================================

#自动在目录下创建log文件夹，并提供write功能
class Log(object):

    def __init__(self):
        self.LoadLog()
        
    def LoadLog(self):
        #检测文件夹是否创建
        if(os.path.exists('./log')==False):
            os.mkdir('./log')


    def write(self,logstr):
        try:
            curtime =  time.localtime(time.time())
            
            FolderRoot = '.\\log\\'        
            filename = str(curtime.tm_year)+'-'+ str(curtime.tm_mon)+'-'+ str(curtime.tm_mday)+'.txt'
            logfilename = FolderRoot+filename
            
            timehead = '['+str(curtime.tm_hour)+':'+str(curtime.tm_min)+':'+str(curtime.tm_sec)+']:'
            content = timehead + logstr
            
            with open(logfilename,'a',encoding='utf-8') as f:
                f.write(content)
                f.write('\n')  
        except:
            print('写入日志失败')
            
            
#testlog = log()
#testlog.write('这是一条日志测试信息')