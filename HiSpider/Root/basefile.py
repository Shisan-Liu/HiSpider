# =============================================================
# Module和Class命名标准：
# ModuleFileName命名必须全小写，允许使用下划线
# Class首字母大写

# EX
# ModuleFileName: base.py
# Class: Base
# =============================================================
# 文件（夹）命名标准：
# DirPath(文件夹路径)前必须有点斜杠 最后必须加斜杠
# FilePath(文件完整路径) 必须由DirPath + FileName.format 拼接

# EX
# dirpath = './t123est/automakedir/test2/'
# filename = 'file.txt'
# filepath = dirpath + filename
# =============================================================
# 函数必须写清楚参数、返回值、功能
# 有Option的需要说明每一个值的作用

# EX
# '''
# Introduce
# Input:
# Return:
# Option:
# '''


import os
import time
import json
class Basefile(object):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)



    def CreateDir(self,tpath,isfilepath=False):
        '''
        Spawn each level dir
        Input: dirpath/filepath(need set isfile=True)
        Return: NULL
        Option: @isfile:default=False,defind tpath is a dirpath
        '''

        targetdictpath = tpath
        if(isfilepath==True):
            targetdictpath = os.path.split(tpath)[0]
        current = './'
        if(os.path.exists(targetdictpath)==False):
            for path in targetdictpath.split('/')[1:]:
                current = current+path+'/'
                if(os.path.exists(current)==False):
                    os.mkdir(current)

    def WriteLine(self,filepath,content):
        '''
        Open file write a line
        '''
        with open(filepath,'a',encoding='utf-8') as f:
            f.write(content)
            f.write('\n')

    def WriteDicToJson(self,filepath,dic):
        '''
        Open .json file write dic
        '''
        self.CreateDir(filepath,True)
        with open(filepath,'w',encoding='utf-8') as file:        
            json_str = json.dumps(dic)
            file.write(json_str)

    def ReadJson(self,filepath):
        '''
        Return dic from json file 
        '''
        dic = {}
        with open(filepath,'r',encoding='utf-8') as file:
            dic = json.loads(file.read())
        return dic


def main():
    test = Base()
    dirpath = "./TestDirPath/"
    filepath = "./TestFilePath/test.txt"
    test.CreateDir(dirpath)
    test.CreateDir(filepath,True)


def main2():
    test = Base()
    josnfilepath = './test/json.json'
    dic = {"key":"value"}
    test.WriteDicToJson(josnfilepath,dic)

if __name__=="__main__":
    print("")
    main2()

