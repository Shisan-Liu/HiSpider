# -*- coding: utf-8 -*-
# =============================================================================
# =============================================================================
# 文件控制器

# 配置文件写入和读取
# 创建完整文件夹
# Diclist写入和读取
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

## 已解决
# 可以创建一个配置文件
# 每个读写的位置，应该在一个地方构造，然后再调用，而不用每一次都调用 名字的构造放在各个具体的位置，filecontroller只负责对文件（夹）的读写
# 抽象：配置文件Save和Load，只负责根据文件名生成和读取文件，不要弄其它处理比如文件路径的构造
# 文件夹的生成可以用一个递归的方式 
# =============================================================================
# =============================================================================
import csv,os,time,sys
from Static.log import Log
import json
# 在Main中一次加载，可以多次读取Conf文件、保存
class FileController(object):
    # 初始化
    def __init__(self,log):
        self.configFilePath = './Config/FileController.conf'      # Save配置文件path
        # 全局环境变量
        self.classname = "FileController"

        #self.contentHome = './content/'               # 文件保存根目录   
        
        self.startLog =  '读取FileController.conf。。。'          # Log信息
        self.endLog = '加载FileController模块。。。OK'

        # 加载Log模块
        self.loclog = log
        self.loclog.write(self.classname+self.startLog)

        # 加载环境变量测试
        try:
            confdic = self.Conf_read(self.configFilePath)
            for k in confdic.keys():
                if(k=='endLog'):
                    self.endLog = confdic[k]
            self.loclog.write("配置文件[%s]创建[成功]"%(self.configFilePath))
        except Exception as result:
            self.loclog.write("配置文件[%s]创建[失败]:%s"%(self.configFilePath,result))
        self.loclog.write(self.classname+self.endLog)

    def CreatDir(self,dirpath):
        # 输入：完整文件夹路径
        # 功能：自动生成每一个文件夹
        # 路径标准：dirpath = './t123est/automakedir/test2'
        try:
            current = './'
            for i,path in enumerate(dirpath.split('/')[1:]):
                current = current+path+'/'
                if(os.path.exists(current)==False):
                    os.mkdir(current)
            self.loclog.write("文件夹[%s]创建[成功]"%(dirpath))
        except Exception as result:
            self.loclog.write("文件夹[%s]创建[失败]:%s"%(dirpath,result))


    def Conf_write(self,filepath,dic):
        # 从字典写入配置文件
        try:
            with open(filepath,'w',encoding='utf-8') as f:        
                for k in dic.keys():
                    f.write(str(k))
                    f.write(' ')                            
                    f.write(dic[k])
                    f.write('\n')
            self.loclog.write("配置文件[%s]保存[成功]"%(filepath))
        except Exception as result:
            self.loclog.write("配置文件[%s]保存[失败]:%s"%(filepath,result))


    def Conf_read(self,filepath):
        # 读取配置文件到字典
        try:
            dic = {}
            with open(filepath,'r',encoding='utf-8') as f:
                for line in f.readlines():
                    if(line[0]!='#'):
                        linecontent = line.split(' ')
                        dic[linecontent[0]] = linecontent[1][0:-1]
            return dic
            self.loclog.write("配置文件[%s]读取[成功]"%(filepath))
        except Exception as result:
            self.loclog.write("配置文件[%s]保存[失败]:%s"%(filepath,result))



    def SaveDicList(self,filename,diclist):
        # 特殊保存方式：两种方式保存Diclist
        className = '__SaveDicList__'
        try:
            format = os.path.splitext(filename)[1]
            with open(filename,'w',encoding='utf-8') as file:
                if(format=='.txt'):
                    for dic in diclist:
                        for k in dic.keys():
                            f.write(str(k)+'_'+dic[k]+' ')
                        f.write('\n')

                elif(format=='.csv'):
                    writer = csv.DictWriter(file,fieldnames=list(diclist[0].keys()))    
                    writer.writeheader()
                    for dic in diclist:
                        writer.writerow(dic)

                elif(format=='.json'):
                    json_str = json.dumps(diclist)
                    file.write(json_str)


            self.loclog.write("%s%s文件[%s]保存[成功]"%(self.classname,className,filename))
        except Exception as result:
            self.loclog.write("%s%s文件[%s]保存[失败]:%s"%(self.classname,className,filename,result))


    def ReadDicList(self,filename):
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

            self.loclog.write("%s%s文件[%s]读取[成功]"%(self.classname,className,filename))
        except Exception as result:
            self.loclog.write("%s%s文件[%s]读取[失败]:%s"%(self.classname,className,filename,result))
        finally:
            print(templist)
            return templist



if __name__=='__main__':
    TestLog = Log()
    TestSave = FileController(TestLog)

    # 配置文件写入和读取
    dic={'endLog':"加载FileController模块。。。OK","contentHome":"./content/"}
    TestSave.Conf_write(TestSave.configFilePath,dic)
    print(TestSave.Conf_read(TestSave.configFilePath))

    # 创建完整文件夹
    TestSave.CreatDir('./content/Test')


    # Diclist写入和读取
    dic1={'time':"1","loc":"12,13"}
    dic2={'time':"2","loc":"1,3"}
    diclist = []
    diclist.append(dic1)
    diclist.append(dic2)
    TestSave.SaveDicList('./content/Test/testjson.json',diclist)
    TestSave.ReadDicList('./content/Test/testjson.json')



