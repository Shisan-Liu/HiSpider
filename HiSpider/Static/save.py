# -*- coding: utf-8 -*-
# 功能
# =============================================================================
# 输入：字典列表,文件夹的名字，保存类型
# 输出：文件夹和txt，CSV两种格式文件
# =============================================================================


# 扩展
# =============================================================================
# 还要储存二进制的文件
# 可以创建一个配置文件
# 后面再弄数据库
# =============================================================================

# 目录结构
# 单网页抓取（通常为首页）
# contentDir
# -ModelNameDir(自定义名称_ParentURL)
# --TempDir(HTML,DataStruct)
# --Config.conf(单网页配置文件)
# --File(index_Time.txt)

# 多网页抓取（根据首页进行大规模爬取）
# contentDir
# -ModelNameDir(自定义名称_ParentURL)
# --OptionNameDir(自定义操作名)
# ---TempDir(HTML,DataStruct)
# ---Config.conf(多网页配置文件)
# ---File(index_ChildURL_Time.txt)

# BUG:
# 配置文件1.用空格分隔很有可能会存在问题2.字符串读取也需要改进3.读取环境变量时即使没有成功读取也不会报错
# 文件夹的生成可以用一个递归的方式 
# 每个读写的位置，应该在一个地方构造，然后再调用，而不用每一次都调用

import csv,os,time,sys
from Static.log import Log

# 在Main中一次加载，可以多次读取Conf文件、保存
class Save(object):
    # 初始化
    def __init__(self,log):
        # 全局环境变量
        self.configFilePath = './Config/Save.conf'      # Save全局配置文件path
        self.contentHome = './content/'               # 文件保存根目录   
        
        self.startLog =  '读取Save.conf。。。'          # Log信息
        self.endLog = '加载Save模块。。。OK'

        #局部环境变量
        #self.Ischeckfolder = False          # 是否检查文件夹创建
        #self.folderPath = ''                # 目标文件夹路径

        # 加载Log模块
        self.loclog = log
        self.loclog.write(self.startLog)

        # 加载环境变量
        self.LoadGlobal()

        self.loclog.write(self.endLog)

    def LoadGlobal(self):
        # 载入配置文件
        try:
            with open(self.configfilepath,'r') as conf:
                for i,line in enumerate(conf.readlines()):
                    try:
                        if(line[0]!='#'):
                            
                            linecontent = line.split(' ')
                            if(linecontent[0]=='configFilePath'):
                                self.configFilePath = linecontent[1]
                            elif(linecontent[0]=='contentHome'):
                                self.contentHome = bool(linecontent[1])
                            elif(linecontent[0]=='startLog'):
                                self.startLog = linecontent[1]
                            elif(linecontent[0]=='endLog'):
                                self.endLog = linecontent[1]
                    except:
                        self.loclog.write('第'+i+'行异常:'+line)

        except Exception as result:
            self.loclog.write(result)

        # 验证环境变量正确性
        # 根目录是否存在
        if(os.path.exists(self.contentHome)==False):
            os.mkdir(self.contentHome)

    def CheckAndMakeDir(self,path):
        # 检查并创建文件夹
        if(os.path.exists(path)==False):
            os.mkdir(path)

    def html_save(self,html,modelname):
        # 将.html文件保存到TEMP文件夹下,返回编号由其模型配置文件记录
        modelHome = self.contentHome+modelname
        self.CheckAndMakeDir(modelHome)
        tempHome = modelHome+'/temp'
        self.CheckAndMakeDir(tempHome)
        htmlHome = tempHome+'/html/'
        self.CheckAndMakeDir(htmlHome)

        num = 0
        path = htmlHome+str(num)+'.html'
        while(os.path.exists(path)==True):
            num+=1
            path = htmlHome+str(num)+'.html'

        with open(path,'w',encoding='utf-8') as f:
            f.write(html)
        return num

    def locConf_save(self,modelname):
        # 保存配置文件
        list = []
        list[0] ='configFilePath'+str(self.configFilePath)
        list[1] ='contentHome'+str(self.contentHome)
        list[2] ='startLog'+str(self.startLog)
        list[3] ='endLog'+str(self.endLog)

        modelHome = self.contentHome+modelname
        self.CheckAndMakeDir(modelHome)
        path = modelHome+'/model.conf'

        with open(path,'w') as conf:
            for line in list:
                conf.write(line)
                conf.write('\n')


    # 检测文件夹是否存在不存在则创建，写入文件
    def content_save(self,modelname,format,diclist):


        filename = self.getFilePath(modelname,format)

        # 调用检测文件夹函数并判断是否成功,失败关闭程序
        if(filename==False):
            self.loclog.write('文件夹名构造异常')
        else:
            # 写入文件
            self.SaveFile(filename,diclist,format)


    # 在content文件夹下创建三级文件夹,一级文件夹以foldername命名，二级以日期命名，三级以次数命名，返回文件夹变量
    def getFilePath(self,modelname,format):
        try:
            # 检查ModelName文件夹是否创建
            htmlHome = self.contentHome+modelname
            if(os.path.exists(htmlHome)==False):
                os.mkdir(htmlHome)

            curtime =  time.localtime(time.time())
            file_sec = str(curtime.tm_year)+'-'+ str(curtime.tm_mon)+'-'+ str(curtime.tm_mday)      
            
            # 文件path
            num = 0
            path = htmlHome+'/'+str(num)+'_'+file_sec+format
            while(os.path.exists(path)==True):num+=1

            return path
        except:
            return False
        
    # 两种方式保存Diclist
    def SaveFile(self,filename,diclist,format):
        try:
            if(format=='.txt'):

                with open(filename,'a',encoding='utf-8') as f:
                    for dic in diclist:
                        for k in dic.keys():
                            f.write(str(k))
                            f.write(' ')                            
                            f.write(dic[k])

                        f.write('\n')

            elif(format=='.csv'):
                with open(filename,'a',encoding='utf-8') as csvfile:
                    keys = []
                    for k in diclist[0].keys():
                        keys.append(k)
                
                    writer = csv.DictWriter(csvfile,fieldnames=keys)    
                    for d in diclist:
                        writer.writerow(d)
                        
            self.loclog.write(filename+' 保存成功')
        except:
            self.loclog.write('打开文件 '+filename+'失败')

if __name__=='__main__':
    TestLog = Log()
    TestSave = Save(TestLog)
    # 保存HTML
    TestSave.html_save('testhtmlcode','testmodelname')
    
    # 保存Diclist
    dic1={'time':"1","loc":"12,13"}
    diclist = []
    diclist.append(dic1)
    TestSave.content_save('writetestmodel','.txt',diclist)

    # 保存配置文件
    TestSave.locConf_save('testsaveconf')