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

from Static.filecontroller import FileController

class Module():
    def __init__(self,modulename):
        self.FC = FileController()
        
        self.confdic = {
            "MoudleName":modulename,
            "ModuleHome":"./content/"+modulename,
            "MoudleTempHome":"./content/"+modulename+"/Temp",
            "MoudleConfHome":"./content/"+modulename+"/Conf",
            "MoudleTempHtmlHome":"./content/"+modulename+"/Temp/Html",
            "confFilePath":"./content/"+modulename+"/Conf"+"/Conf.conf",
            "testcontent":""
            }

        #  加载或创建各配置文件
        # 调用流程：
        # 创建时，生成配置文件夹并使用默认字典生成配置文件
        # 打开时，用配置文件中的变量初始化字典
        self.FC.Conf_load(self.confdic)
        # 检测并创建某些文件目录
        self.FC.CreateDir(self.confdic["MoudleTempHtmlHome"])
        self.html={
            "confFilePath":self.confdic["MoudleConfHome"]+"/html.conf",
            "sourcePath":self.confdic["MoudleTempHtmlHome"]+'/source.html',
            "source":""
            }
        # 创建这个配置文件的目的是记录生成的文件的path，以便打开
        self.FC.Conf_load(self.html)
        self.diclist = {
            "confFilePath":self.confdic["MoudleConfHome"]+"/diclist.conf",
            "diclistPath":"",
            "diclist":[]
            }
        self.FC.Conf_load(self.diclist)


    def Confdic_get(self):
        # 获取配置文件dic进行修改，还需要再封装一个edit应用层
        return self.FC.Conf_read(self.confdic["confFilePath"])

    def Confdic_set(self,dic):
        # 修改读取的confdic后调用保存修改，并刷新当前配置
        self.FC.Conf_write(dic)     
        self.confdic = dic

    # 使用流程：
    # 创建时 set Html_Source（保存到内存）==> save（保存到本地）
    # 打开时 html = Html_Source_get(self)（并在内存中记录self.html["source"]）
    def Html_Source_set(self,html):
        # 设置html[source]
        self.html["source"] = html

    def Html_Source_save(self):
        # 保存HTML字典中源代码到指定文件
        self.FC.File_write(self.html["sourcePath"],self.html["source"])
    def Html_Source_get(self):
        # 获取（并用保存的文件设置）html[source]
        if(self.html["source"] == ""):
            self.html["source"] = self.FC.File_read(self.html["sourcePath"])
        return self.html["source"]

    # 使用流程：
    # 创建时 首先调用set设置此实例的self.diclist["diclist"] 再保存到本地并设置path，更新配置文件
    def Diclist_set(self,diclist):
        self.diclist["diclist"] = diclist
    def Diclist_save(self,filename):
        # 保存到文件并设置path
        # filename = 名字.后缀
        path = self.confdic["ModuleHome"]+'/'+filename
        
        # 修改配置文件中的path和变量
        tempdic = self.FC.Conf_read(self.diclist["confFilePath"])
        tempdic["diclistPath"]=path
        self.FC.Conf_write(tempdic)
        self.diclist["diclistPath"] = path

        self.FC.DicList_write(path,self.diclist["diclist"])

    def Diclist_get(self):
        if(self.diclist["diclist"]==""):
            self.diclist["diclist"] = self.FC.DicList_read(self.diclist["diclistPath"])
        return self.diclist["diclist"]

    
    #def Conf_edit(self,sourcedic)
    #编辑配置文件，可以用回调函数

if __name__=='__main__':

    baidu = Module("baidu")
    #配置文件修改流程
    tempdic = baidu.Confdic_get()
    print(tempdic)
    tempdic["testcontent"] = "在UI或文件中修改"
    baidu.Confdic_set(tempdic)
    print(baidu.confdic)

    # 创建模型，需要set并saveHTML源代码
    baidu.Html_Source_set('这是一段完整的html代码')#  设置
    baidu.Html_Source_save()
    print(baidu.Html_Source_get())# 获取之后在UI或者命令行中显示


    # Diclist写入和读取
    dic1={'time':"1","loc":"12,13"}
    dic2={'time':"2","loc":"1,3"}
    diclist = []
    diclist.append(dic1)
    diclist.append(dic2)

    filename1 = '1.json'

    baidu.Diclist_set(diclist)
    print(baidu.diclist["diclist"])

    baidu.Diclist_save(filename1)
    print(baidu.Diclist_get())






'''
baidu = Module("baidu")

print(baidu.Html_Source_get())

print(baidu.diclist["diclist"])

print(baidu.Diclist_get())
'''