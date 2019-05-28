
# 捕捉异常并进行处理Decorator
def catch_exception(func):
    def wrapper(self,*args,**kw):
        try:

            return func(self,*args,**kw)
        except Exception:
            error = func.__name__ + "错误"
            self.Log_write(error,2)

            return ""
    return wrapper



from Root.basefile import *

class FileController(Basefile):

    def __init__(self, *args, **kwargs):
        self.__confdic = {
                "confFilePath":'./Config/FileController.json',
                "LogHome":'./log/'
        }
        self.Conf_load(self.__confdic)
        return super().__init__(*args, **kwargs)

    @catch_exception
    def Log_write(self,logstr,type=0):
        '''
        Add a loginfo(error,normal,worring...) to logfile
        Input:logstring
        OutPut:NULL
        Option: @type:defualt=0 Normal;type=1 Worring;type=2 Error
        '''
        curtime =  time.localtime(time.time())
        logfilename = self.__confdic["LogHome"]+str(curtime.tm_year)+'-'+ str(curtime.tm_mon)+'-'+ str(curtime.tm_mday)+'.txt'
        self.CreateDir(logfilename,True)
        content = '[' + str(curtime.tm_hour)+ ':' + str(curtime.tm_min) + ':' + str(curtime.tm_sec) + ']:'
        if(type==1):
            content = content+"Worring:"
        elif(type==2):
            content = content+"Error:"
        content = content+ str(logstr)
        self.WriteLine(logfilename,content)

    @catch_exception
    def Conf_write(self,confdic):
        '''
        Write or Update confdic into confdic[confFilePath]
        '''
        filepath = confdic["confFilePath"]
        self.WriteDicToJson(filepath,confdic)

    @catch_exception
    def Conf_read(self,confdic):
        '''
        Return confdic
        '''
        filepath = confdic["confFilePath"]
        return self.ReadJson(filepath)

    @catch_exception
    def Conf_load(self,confdic):
        '''
        if conffile exist read,else create
        '''
        filepath = confdic["confFilePath"]
        if(os.path.exists(filepath)==False):
            self.Conf_write(confdic)
        else:
            fileconfdic = self.Conf_read(confdic)
            for k in fileconfdic.keys():
                confdic[k] = fileconfdic[k]



    @catch_exception
    def Conf_edit(self,confdic,key,value):
        # 这里其实没有必要重写整个文件
        '''
        Edit a confdic value
        '''
        tempdic = self.Conf_read(confdic)
        tempdic[key] = value
        for k in tempdic.keys():
            confdic[k] = tempdic[k]
        self.Conf_write(tempdic)

    @catch_exception
    def WriteNormal(self,filepath,content,encode = 'utf-8'):
        '''
        Write a file
        '''
        self.CreateDir(filepath,True)
        with open(filepath,'w',encoding=encode) as f:
            f.write(str(content))

    @catch_exception
    def ReadNormal(self,filepath,encode = 'utf-8'):
        '''
        Return filestr
        '''
        if(os.path.exists(filepath)==True):
            with open(filename,'r',encoding=code) as f:
                return f.read()
        else:
            return ""

    @catch_exception
    def DicList_write(self,filename,diclist):
        '''
        Write a diclist
        '''
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


    @catch_exception
    def DicList_read(self,filename):
        '''
        Return a diclist
        '''
        templist = []
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
        return templist



def main():
    test = FileController()
    test.Log_write("123",1)



if __name__=="__main__":
    main()