from Static.filecontroller import FileController

# 抓取数据模型
class Module():
    def __init__(self,modulename):
        self.confdic = {
            "MoudleName":modulename,
            "ModuleHome":"./content/"+modulename,
            "confFilePath":"./content/"+modulename+"/Conf/Conf.json",

            "url":"",

            "html":"",
            "htmlPath":"./content/"+modulename+"/Html/source.html",
            "htmlcode":"utf-8",

            "diclist":[],
            "diclistPath":""
            }

        # 加载或创建各配置文件
        self.FC = FileController()
        self.FC.Conf_load(self.confdic)

    def GetValue(self,key):
        return self.confdic[key]    

    def SetValue(self,key,value):
        self.FC.Conf_edit(self.confdic,key,value)

    def SetUHF(self,url,html,htmlcode):

        self.SetValue("url",url)
        self.SetValue("html",html)
        self.SetValue("htmlcode",htmlcode)

        # 保存HTML文件
        self.FC.File_write(self.confdic["htmlPath"],self.confdic["html"],self.confdic["htmlcode"])

    def SaveDiclist(self,filename):
        # 保存整个diclist
        # 设置path并保存到文件:filename = 名字.后缀
        diclistpath = self.confdic["ModuleHome"]+'/'+filename
        self.SetValue("diclistPath",diclistpath);
        self.FC.DicList_write(diclistpath,self.confdic["diclist"])




if __name__=='__main__':
    # 创建、设置、保存
    print()

# =============================================================================
# 模型结构

# 单网页抓取（主页和文章页）
# contentDir
# -ModelNameDir(自定义名称_ParentURL)
# --Html/html.html
# --Conf/conf.conf
# --Content.txt/json/csv

# 多网页后面再进行设计
# =============================================================================