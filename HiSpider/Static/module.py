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
        self.confdic = {
            "confFilePath":"./content/"+modulename+"/Conf/Conf.json",

            "MoudleName":modulename,

            "ModuleHome":"./content/"+modulename,

            "url":"",
            "format":"",
            #HTML
            "MoudleTempHtmlHome":"./content/"+modulename+"/Html",
            "htmlPath":"./content/"+modulename+"/Html/source.html",
            "html":"",
            #Diclist
            "htmlcode":"utf-8",
            "diclist":[]
            }

        #  加载或创建各配置文件
        self.FC = FileController()
        self.FC.Conf_load(self.confdic)

    def GetValue(self,key):
        return self.confdic[key]    

    def SetUHF(self,url,html,format,htmlcode):
        self.FC.Conf_edit(self.confdic,"url",url)
        self.FC.Conf_edit(self.confdic,"html",str(html))
        self.FC.Conf_edit(self.confdic,"format",format)
        self.FC.Conf_edit(self.confdic,"htmlcode",htmlcode)
        self.FC.File_write(self.confdic["htmlPath"],self.confdic["html"],self.confdic["htmlcode"])


    def SetDiclist(self,diclist):
        self.FC.Conf_edit(self.confdic,"diclist",diclist)

    def SaveDiclist(self,filename):
        # 设置path并保存到文件:filename = 名字.后缀
        path = self.confdic["ModuleHome"]+'/'+filename
        
        self.FC.Conf_edit(self.confdic,"confFilePath",path)
        self.FC.DicList_write(path,self.confdic["diclist"])




if __name__=='__main__':
    # 创建模型
    baidu = Module("ModuleTest")


    #设置HTML以显示(FC.Conf_edit测试)
    baidu.SetHtml('这是一段完整的html代码')
    #获取HTML
    print(baidu.GetHtml())
    #保存HTML（FC.File_write测试）
    baidu.SaveHtml()

    dic1={'time':"1","loc":"12,13"}
    dic2={'time':"2","loc":"1,3"}
    diclist = []
    diclist.append(dic1)
    diclist.append(dic2)

    filename1 = '1.json'

    #设置Diclist
    baidu.SetDiclist(diclist)
    #获取Diclist
    print(baidu.GetDiclist())
    #保存Diiclist
    baidu.SaveDiclist(filename1)
    #print(baidu.confdic)
