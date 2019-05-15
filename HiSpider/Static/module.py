# =============================================================================
# =============================================================================
# 这个模型便是一次抓取模型
# 保存各种信息变量
# 抓取数据后生成，UI显示 数据时读取保存方法
# =============================================================================
# =============================================================================
# 模型结构

# 单网页抓取（通常为首页）
# contentDir
# -ModelNameDir(自定义名称_ParentURL)
# --TempDir(HTML,DataStruct等临时文件)
# --Config.conf(单网页配置文件)
# --File(index_Time.txt)
# 多网页抓取（根据首页进行大规模爬取）
# --OptionNameDir(自定义操作名)
# ---TempDir(HTML,DataStruct)
# ---Config.conf(多网页操作配置文件)
# ---File(index_ChildURL_Time.txt)
# =============================================================================
# =============================================================================



from Static.filecontroller import FileController as FC
from Static.log import Log
class Model(object):
    def __init__(self,modelname):
        self.classname = "Model_"+modelname
        self.startLog =  '=====================读取'+modelname+'.conf。。。====================='          # Log信息
        self.endLog = '=====================加载'+modelname+'成功====================='

        self.html = ''
        self.diclist = []                               #最终字典列表

        self.contentHome = './content/'                 # 文件保存根目录  
        self.modelHome = ''
        self.tempHome = ''
        self.htmlHome = ''

        # 加载Log模块
        self.loclog = Log()
        # 开始初始化
        self.loclog.write(self.classname+self.startLog)
        # 加载文件控制器模块
        self.fileController = FC()
        # 加载配置文件测试
        try:
            confdic = self.Conf_read(self.configFilePath)
            for k in confdic.keys():
                if(k=='endLog'):
                    self.endLog = confdic[k]
            self.loclog.write("配置文件[%s]创建[成功]"%(self.configFilePath))
        except Exception as result:
            self.loclog.write("配置文件[%s]创建[失败]:%s"%(self.configFilePath,result))
        # 结束初始化
        self.loclog.write(self.classname+self.endLog)


    




    def SaveConf(self,contentHome,modelname):
        # 配置文件,创建模型文件夹，写入配置文件
        className = "locConf_save_"+modelname+'_'

        self.modelHome = contentHome+modelname       #ModelHome
        self.CheckAndMakeDir(modelHome)
        self.tempHome = modelHome+'/temp'            #tempHome
        self.CheckAndMakeDir(tempHome)
        self.htmlHome = tempHome+'/html/'            #htmlHome
        self.CheckAndMakeDir(htmlHome)

        try:
            list = []
            list.append('modelHome '+ self.modelHome)
            list.append('tempHome '+ self.tempHome)
            list.append('htmlHome '+ self.htmlHome)


            path = self.modelHome+'/model.conf'

            with open(path,'w') as conf:
                for line in list:
                    conf.write(line)
                    conf.write('\n')
            self.loclog.write("%s%s配置文件[%s]保存[成功]"%(self.classname,className,path))
        except Exception as result:
            self.loclog.write("%s%s配置文件[%s]保存[失败]:%s"%(self.classname,className,path,result))


    def LoadConf(self,contentHome,modelname):

        path = contentHome+modelname+'/model.conf'
        with open(path,'r') as f:
            for i,line in enumerate(f.readlines()):
                try:
                    if(line[0]!='#'):
                        linecontent = line.split(' ')
                        if(linecontent[0]=='modelHome'):
                            self.modelHome = linecontent[1][0:-1]
                            print(modelHome)
                        elif(linecontent[0]=='tempHome'):
                            self.tempHome = linecontent[1][0:-1]
                            print(tempHome)
                        elif(linecontent[0]=='htmlHome'):
                            self.htmlHome = linecontent[1][0:-1]
                            print(htmlHome)
                except:
                    self.loclog.write(self.classname+className+'第'+i+'行异常:'+line)

    def html_save(self,html,modelname):
        # 将.html文件保存到TEMP文件夹下,返回编号由其模型配置文件记录
        className = "HtmlSaver_"+modelname+'_'

        if(self.CheckLocConfig()):
            #如果有配置文件就直接从配置文件中获取路径

        else:
            self.locConf_save()
            #否则调用locConf_save函数创建文件夹和配置文件，再从配置文件中读取

        modelHome = self.contentHome+modelname
        self.CheckAndMakeDir(modelHome)
        tempHome = modelHome+'/temp'
        self.CheckAndMakeDir(tempHome)
        htmlHome = tempHome+'/html/'
        self.CheckAndMakeDir(htmlHome)
        
        num = 0
        path = htmlHome+str(num)+'.html'

        try:
            while(os.path.exists(path)==True):
                num+=1
                path = htmlHome+str(num)+'.html'

            with open(path,'w',encoding='utf-8') as f:
                f.write(html)
            self.loclog.write("%s%sHTML[%s]保存[成功]"%(self.classname,className,path))
            return num

        except Exception as result:
            self.loclog.write("%s%sHTML[%s]保存[失败]:"%(self.classname,className,path,result))

    def content_save(self,modelname,format,diclist):
        # 构造文件path并调用保存DiclistContent
        htmlHome = self.contentHome+modelname
        self.CheckAndMakeDir(htmlHome)
        # 取消Index+time命名
        #curtime =  time.localtime(time.time())
        #file_sec = str(curtime.tm_year)+'-'+ str(curtime.tm_mon)+'-'+ str(curtime.tm_mday)      
        num = 0
        path = htmlHome+'/'+str(num)+format
        while(os.path.exists(path)==True):
            num+=1
            path = htmlHome+'/'+str(num)+format
        if(path==False):self.loclog.write('文件夹名构造异常')
        else:self.SaveFile(path,diclist,format)

if __name__=='__main__':
    TestLog = Log()
    TestSave = FileController(TestLog)