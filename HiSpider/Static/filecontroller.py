# -*- coding: utf-8 -*-

import csv,os,time,sys,json

class FileController(object):
    # 初始化
    def __init__(self):
        self.confdic = {
                "confFilePath":'./Config/FileController.json',
                "logHome":'./log',
            }

        # 加载Log模块
        self.CreateDir(self.confdic["logHome"])
        # 加载配置文件
        self.Conf_load(self.confdic)

    def File_write(self,filename,content,encode = "utf-8"):
        # 普通字符串读写
        #try:
        self.CreateDirFromPath(filename)
        with open(filename,'w',encoding=encode) as f:
            f.write(str(content))
        self.Log_write("文件[%s]创建[成功]"%(filename))
        #except Exception as result:
            #self.Log_write("文件[%s]创建[失败]:%s"%(filename,result))

    def File_read(self,filename,code="utf-8"):
        # 普通字符串读写
        #try:
        content=''
        with open(filename,'r',encoding=code) as f:
            content = f.read()
        return content
            #self.Log_write("文件[%s]读取[成功]"%(filename))
        #except Exception as result:
            #self.Log_write("文件[%s]读取[失败]:%s"%(filename,result))


    def Log_write(self,logstr):
        # 输入：写入Log文件
        # 功能：遍历生成完整路径
        curtime =  time.localtime(time.time())
        # 文件路径
        logfilename = self.confdic["logHome"]+'/'+str(curtime.tm_year)+'-'+ str(curtime.tm_mon)+'-'+ str(curtime.tm_mday)+'.txt'
        # 内容 = 时间戳+信息
        content = '[' + str(curtime.tm_hour)+ ':' + str(curtime.tm_min) + ':' + str(curtime.tm_sec) + ']:' + str(logstr)
        with open(logfilename,'a',encoding='utf-8') as f:
            f.write(content)
            f.write('\n')  

    def CreateDirFromPath(self,path):
        #根据完整文件path创建文件夹
        # 路径标准：dirpath = './t123est/automakedir/test2/test.html'
        self.CreateDir(os.path.split(path)[0])

    def CreateDir(self,dirpath):
        # 输入：完整文件夹路径
        # 功能：生成完整路径
        # 路径标准：dirpath = './t123est/automakedir/test2'
        #try:
        current = './'
        if(os.path.exists(dirpath)==False):
            for i,path in enumerate(dirpath.split('/')[1:]):
                current = current+path+'/'
                if(os.path.exists(current)==False):
                    os.mkdir(current)
                    ismake = True
            self.Log_write("文件夹[%s]创建[成功]"%(dirpath))
            #else:
                #self.Log_write("文件夹[%s][已创建]" %(dirpath))
        #except Exception as result:
            #self.Log_write("文件夹[%s]创建[失败]:%s"%(dirpath,result))


    def Conf_load(self,confdic):
        # 加载配置文件
        confpath = confdic["confFilePath"]
        #try:
        if(os.path.exists(confpath)==False):
            self.CreateDirFromPath(confpath)
            self.Conf_write(confdic)                    #默认字典写入配置文件
            self.Log_write("配置文件[%s]创建[成功]"%(confpath))
        else:
            fileconfdic = self.Conf_read(confdic)
            confdic = fileconfdic

            self.Log_write("配置文件[%s]加载[成功]"%(confpath))
        #except Exception as result:
            #self.Log_write("加载配置文件[%s][错误]:%s"%(confpath,result))




    def Conf_write(self,confdic):
        path = confdic["confFilePath"]
        # 从字典写入配置文件
        #try:
        with open(path,'w',encoding='utf-8') as file:        
            json_str = json.dumps(confdic)
            file.write(json_str)

            self.Log_write("配置文件[%s]写入[成功]"%(path))
        #except Exception as result:
            #self.Log_write("配置文件[%s]写入[失败]:%s"%(path,result))


    def Conf_read(self,confdic):

        path = confdic["confFilePath"]
        # 读取配置文件到字典，出现任何问题将返回空字典
        dic = {}
        #try:
        with open(path,'r',encoding='utf-8') as file:
            dic = json.loads(file.read())
            
            self.Log_write("配置文件[%s]读取[成功]"%(path))
        #except Exception as result:
            #self.Log_write("配置文件[%s]读取[失败]:%s"%(path,result))
        #finally:
        return dic


    def Conf_edit(self,confdic,key,value):
        #配置文件修改
        tempdic = self.Conf_read(confdic)
        tempdic[key] = value
        for k in tempdic.keys():
            confdic[k] = tempdic[k]
        self.Conf_write(tempdic)

    def DicList_write(self,filename,diclist):

        #try:
        format = self.GetFileFormat(filename)
        with open(filename,'w',encoding='utf-8',newline="") as file:
            if(format=='.csv'):
                writer = csv.DictWriter(file,fieldnames=list(diclist[0].keys()))    
                writer.writeheader()
                for dic in diclist:
                    writer.writerow(dic)

            elif(format=='.json'):
                json_str = json.dumps(diclist)
                file.write(json_str)

            #self.Log_write("%s%s文件[%s]保存[成功]"%(self.confdic["className"],className,filename))
        #except Exception as result:
            #self.Log_write("%s%s文件[%s]保存[失败]:%s"%(self.confdic["className"],className,filename,result))
    def GetFileFormat(self,path):
        return os.path.splitext(path)[1]

    def DicList_read(self,filename):
        # 读取DicList
        templist = []

        #try:
        format = self.GetFileFormat(filename)
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

            #self.Log_write("%s%s文件[%s]读取[成功]"%(self.confdic["className"],className,filename))
        #except Exception as result:
            #self.Log_write("%s%s文件[%s]读取[失败]:%s"%(self.confdic["className"],className,filename,result))
        #finally:
            #print(templist)
        return templist


if __name__=='__main__':
    fc = FileController()
    print(fc.GetFileFormat("/sgdsg/qwe.txt"))
    print(fc.GetFileFormat("wer"))