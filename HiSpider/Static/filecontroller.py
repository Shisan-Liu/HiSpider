# -*- coding: utf-8 -*-
# =============================================================================
# =============================================================================
# 文件控制器

# 配置文件写入和读取，加载
# 创建完整文件夹
# 内容Diclist写入和读取
# =============================================================================
# =============================================================================
# 扩展

# 储存二进制的文件
# 数据库

# =============================================================================
# =============================================================================
# BUG:
# 配置文件1.用空格分隔很有可能会存在问题2.字符串读取也需要改进

# 问题
# .txt的存储格式有待提高
# .csv读取函数还没有写

# 配置文件和临时文件使用字典格式
# 导出文件使用根据需求使用csv或者其它格式

## 已解决
# 可以创建一个配置文件
# 每个读写的位置，应该在一个地方构造，然后再调用，而不用每一次都调用 名字的构造放在各个具体的位置，filecontroller只负责对文件（夹）的读写
# 抽象：配置文件Save和Load，只负责根据文件名生成和读取文件，不要弄其它处理比如文件路径的构造
# 文件夹的生成可以用一个递归的方式 
# =============================================================================
# =============================================================================
import csv,os,time,sys,json

class FileController(object):
    # 初始化
    def __init__(self):
        self.confdic = {
            "confFilePath":'./Config/FileController.conf',
            "logHome":'./log',
            "className":"FileController",
            "logstart":'Log模块。。。OK',
            "endLog":'=====================FileController模块。。。OK=====================',
            "startLog":'=====================加载FileController.conf。。。====================='
            }

        # 加载Log模块
        self.CreateDir(self.confdic["logHome"])
        # 加载配置文件
        self.Conf_load(self.confdic)


    def File_write(self,filename,content):
        try:
            with open(filename,'w',encoding='utf-8') as f:
                f.write(content)
            self.Log_write("文件[%s]创建[成功]"%(filename))
        except Exception as result:
            self.Log_write("文件[%s]创建[失败]:%s"%(filename,result))

    def File_read(self,filename):
        try:
            content=''
            with open(filename,'r',encoding='utf-8') as f:
                content = f.read()
            return content
            self.Log_write("文件[%s]读取[成功]"%(filename))
        except Exception as result:
            self.Log_write("文件[%s]读取[失败]:%s"%(filename,result))


    def Log_write(self,logstr):
        # 写入Log文件
        curtime =  time.localtime(time.time())
        # 文件路径
        logfilename = self.confdic["logHome"]+'/'+str(curtime.tm_year)+'-'+ str(curtime.tm_mon)+'-'+ str(curtime.tm_mday)+'.txt'
        # 内容 = 时间戳+信息
        content = '[' + str(curtime.tm_hour)+ ':' + str(curtime.tm_min) + ':' + str(curtime.tm_sec) + ']:' + str(logstr)
        with open(logfilename,'a',encoding='utf-8') as f:
            f.write(content)
            f.write('\n')  

    def CreateDir(self,dirpath):
        # 输入：完整文件夹路径
        # 功能：遍历生成完整路径
        # 路径标准：dirpath = './t123est/automakedir/test2'
        try:
            current = './'
            if(os.path.exists(dirpath)==False):
                for i,path in enumerate(dirpath.split('/')[1:]):
                    current = current+path+'/'
                    if(os.path.exists(current)==False):
                        os.mkdir(current)
                        ismake = True
                self.Log_write("文件夹[%s]创建[成功]"%(dirpath))
            else:
                self.Log_write("文件夹[%s][已创建]" %(dirpath))
        except Exception as result:
            self.Log_write("文件夹[%s]创建[失败]:%s"%(dirpath,result))


    def Conf_load(self,confdic):
        # 加载配置文件，需要在全局变量中创建字典以使用
        # 如果配置文件不存在，就创建配置文件并把默认字典写入到配置文件
        # 如果配置文件存在，就把配置文件中信息写入字典
        confpath = confdic["confFilePath"]
        try:
            if(os.path.exists(confpath)==False):
                self.CreateDir(os.path.split(confpath)[0])  #不用担心文件夹没有创建，这里会自动检测
                self.Conf_write(confdic)       #默认字典写入配置文件

            else:
                fileconfdic = self.Conf_read(confpath)
                for k in fileconfdic.keys():
                    for confkey in confdic.keys():
                        if(k==confkey):
                            confdic[k] = fileconfdic[k]     #改变默认字典
                self.Log_write("配置文件[%s]加载[成功]"%(confpath))

        except Exception as result:
            self.Log_write("加载配置文件[%s][错误]:%s"%(confpath,result))



    def Conf_write(self,confdic):
        confpath = confdic["confFilePath"]
        # 从字典写入配置文件
        try:
            with open(confpath,'w',encoding='utf-8') as f:        
                for k in confdic.keys():
                    f.write(str(k))
                    f.write(' ')                            
                    f.write(confdic[k])
                    f.write('\n')
            self.Log_write("配置文件[%s]写入[成功]"%(confpath))
        except Exception as result:
            self.Log_write("配置文件[%s]写入[失败]:%s"%(confpath,result))


    def Conf_read(self,filepath):
        # 读取配置文件到字典，出现任何问题将返回空字典
        dic = {}
        try:
            with open(filepath,'r',encoding='utf-8') as f:
                for line in f.readlines():
                    if(line[0]!='#'):
                        linecontent = line.split(' ')
                        dic[linecontent[0]] = linecontent[1][0:-1]
            
            self.Log_write("配置文件[%s]读取[成功]"%(filepath))
        except Exception as result:
            self.Log_write("配置文件[%s]读取[失败]:%s"%(filepath,result))
        finally:return dic


    def DicList_write(self,filename,diclist):
        # 特殊保存方式：两种方式保存Diclist
        className = '__SaveDicList__'
        try:
            format = os.path.splitext(filename)[1]
            with open(filename,'w',encoding='utf-8',newline="") as file:
                if(format=='.csv'):
                    writer = csv.DictWriter(file,fieldnames=list(diclist[0].keys()))    
                    writer.writeheader()
                    for dic in diclist:
                        writer.writerow(dic)

                elif(format=='.json'):
                    json_str = json.dumps(diclist)
                    file.write(json_str)

            self.Log_write("%s%s文件[%s]保存[成功]"%(self.confdic["className"],className,filename))
        except Exception as result:
            self.Log_write("%s%s文件[%s]保存[失败]:%s"%(self.confdic["className"],className,filename,result))


    def DicList_read(self,filename):
        # 读取DicList
        templist = []
        className = '__ReadDicList__'
        try:
            format = os.path.splitext(filename)[1]
            with open(filename,'r',encoding='utf-8') as file:
                if(format=='.txt'):
                
                    for line in file.readlines():
                        dic = {}
                        for item in line.split(' '):
                            kvs = item.split('_')
                            if(len(kvs)>=2 and kvs[0]!=' ' and kvs[1]!=' '):
                                k = kvs[0]
                                v = kvs[1]
                                dic[k] = v
                        templist.append(dic)


                #elif(format=='.csv'):
                elif(format=='.json'):
                    templist = json.loads(file.read())

            self.Log_write("%s%s文件[%s]读取[成功]"%(self.confdic["className"],className,filename))
        except Exception as result:
            self.Log_write("%s%s文件[%s]读取[失败]:%s"%(self.confdic["className"],className,filename,result))
        finally:
            #print(templist)
            return templist