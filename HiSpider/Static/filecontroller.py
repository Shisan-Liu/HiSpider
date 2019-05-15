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
from Static.log import Log


class FileController(object):
    # 初始化
    def __init__(self):
        self.configFilePath = './Config/FileController.conf'      # Save配置文件path
        self.confdic = {
            "className":"FileController",
            "endLog":'=====================加载FileController模块。。。OK=====================',
            "startLog":'=====================读取FileController.conf。。。====================='
            }
        # 加载Log模块
        self.loclog = Log()
        # 开始初始化
        self.loclog.write(self.confdic["className"]+self.confdic["startLog"])

        # 加载配置文件
        self.Conf_load(self.confdic)
        # 结束初始化
        self.loclog.write(self.confdic["className"]+self.confdic["endLog"])

    def CreatDir(self,dirpath):
        # 输入：完整文件夹路径
        # 功能：遍历生成完整路径
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


    def Conf_load(self,confdic):
        # 加载配置文件，需要在全局变量中创建字典以使用
        try:
            confdic = {}
            confdic = self.Conf_read(self.configFilePath)
            if(confdic!={}):
                for k in confdic.keys():
                    for confkey in confdic.keys():
                        if(k==confkey):
                            confdic[k] = confdic[k]
                self.loclog.write("配置文件[%s]创建[成功]"%(self.configFilePath))
            else:
                self.CreatDir(os.path.split(self.configFilePath)[0])
                self.loclog.write("读取配置文件[%s][异常]，已创建配置文件"%(self.configFilePath))
        except Exception as result:
            self.loclog.write("配置文件[%s]创建[错误]:%s"%(self.configFilePath,result))



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
        # 读取配置文件到字典，出现任何问题将返回空字典
        dic = {}
        try:
            with open(filepath,'r',encoding='utf-8') as f:
                for line in f.readlines():
                    if(line[0]!='#'):
                        linecontent = line.split(' ')
                        dic[linecontent[0]] = linecontent[1][0:-1]
            
            self.loclog.write("配置文件[%s]读取[成功]"%(filepath))
        except Exception as result:
            self.loclog.write("配置文件[%s]保存[失败]:%s"%(filepath,result))
        finally:return dic


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

            self.loclog.write("%s%s文件[%s]保存[成功]"%(self.confdic["className"],className,filename))
        except Exception as result:
            self.loclog.write("%s%s文件[%s]保存[失败]:%s"%(self.confdic["className"],className,filename,result))


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

            self.loclog.write("%s%s文件[%s]读取[成功]"%(self.confdic["className"],className,filename))
        except Exception as result:
            self.loclog.write("%s%s文件[%s]读取[失败]:%s"%(self.confdic["className"],className,filename,result))
        finally:
            #print(templist)
            return templist



if __name__=='__main__':

    TestSave = FileController()

    # 配置文件写入和读取
    dic={'endLog':"加载FileController模块。。。OK","contentHome":"./content/"}
    TestSave.Conf_write(TestSave.configFilePath,dic)
    #print(TestSave.Conf_read(TestSave.configFilePath))

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

    configFilePath = './content/Test/testjson.json'
    #print(os.path.split(configFilePath)[0])



