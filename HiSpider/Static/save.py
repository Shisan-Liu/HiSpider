# -*- coding: utf-8 -*-
# 功能
# =============================================================================
# 输入：字典列表,文件夹的名字，保存类型
# 输出：文件夹和txt，CSV两种格式文件
# =============================================================================

# 流程
# =============================================================================
# 先检测文件夹是否存在，再写入文件
# =============================================================================

# 扩展
# =============================================================================
# 还要储存二进制的文件
# 可以创建一个配置文件
# 后面再弄数据库
# =============================================================================

import csv,os,time,sys
import log
class Save(object):
    # 初始化
    def __init__(self):
        # 写入日志
        self.loclog = log.Log()
        self.loclog.write('Save模块载入成功')
        self.ischeckfolder = False
        # 根目录
        self.FolderRoot = '.\\content\\'
        # 目标文件夹路径
        self.folderpath = ''
    
    
    # 检测文件夹是否存在不存在则创建，写入文件
    def write(self,foldername,filename,diclist,filetype):
        
        # 判断是否已经检查过文件夹
        if(self.ischeckfolder==False):
            
            # 调用检测文件夹函数并判断是否成功,失败关闭程序
            if(self.CheckFolder(foldername)==False):
                self.loclog.write('文件夹检测或创建失败')
            else:
                self.ischeckfolder = True
                self.loclog.write(self.folderpath +'文件夹已创建'+'开始写入文件')
        # 写入文件
        self.SaveFile(filename,diclist,filetype)


    # 在content文件夹下创建三级文件夹,一级文件夹以foldername命名，二级以日期命名，三级以次数命名，返回文件夹变量
    def CheckFolder(self,foldername):
        try:
            # 一级文件夹：根目录+根据抓取网站设置的名字
            firFolderPath = self.FolderRoot+foldername
            if(os.path.exists(firFolderPath)==False):
                os.mkdir(firFolderPath)
            
            curtime =  time.localtime(time.time())
            foldername_sec = str(curtime.tm_year)+'-'+ str(curtime.tm_mon)+'-'+ str(curtime.tm_mday)
            
            # 二级文件夹 日期
            secFolderPath = firFolderPath+'\\'+foldername_sec
            if(os.path.exists(secFolderPath)==False):
                os.mkdir(secFolderPath)
            
            # 三级目录 第几次抓取
            num = 0
            while(os.path.exists(secFolderPath+'\\'+str(num))==True):num+=1
                
            # 最终目录
            self.folderpath = secFolderPath+'\\'+str(num)
            os.mkdir(self.folderpath)
            
            return True
        except:
            return False
        
    # 两种保存方式
    def SaveFile(self,filename,diclist,filetype):
        
        # 文件路径 = 文件夹路径+文件名
        filepath = self.folderpath+'\\'+filename+filetype
        
        try:
            if(filetype=='.txt'):

                with open(filepath,'a',encoding='utf-8') as f:
                    for dic in diclist:
                        for k in dic.keys():
                            f.write(str(k))
                            f.write(' ')                            
                            f.write(dic[k])

                        f.write('\n')

            elif(filetype=='.csv'):
                with open(filepath,'a',encoding='utf-8') as csvfile:
                    keys = []
                    for k in diclist[0].keys():
                        keys.append(k)
                
                    writer = csv.DictWriter(csvfile,fieldnames=keys)    
                    for d in diclist:
                        writer.writerow(d)
                        
            self.loclog.write(filename+' 保存成功')
        except:
            self.loclog.write('打开文件 '+filename+'失败')