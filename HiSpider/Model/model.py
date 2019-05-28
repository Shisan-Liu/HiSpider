# 抓取模型



from Root.filecontroller import FileController

class Model(FileController):
    def __init__(self,*args, **kwargs):
        self.__confdic = {
                "ModelName":args[0],
                "ModelHome":"./content/"+args[0]+'/',
                "confFilePath":"./content/"+args[0]+"/Conf/Conf.json",
                "HtmlFilePath":"./content/"+args[0]+"/temp/html.html",
                "HtmlCode":"",

                "url":"",
                "html":"",
                "diclist":{}
        }

        self.Conf_load(self.__confdic)

        return super().__init__()

    def GetConfDic(self):
        return self.__confdic

    def Get(self,key):
        return self.__confdic[key]    

    def Set(self,key,value):
        # 在类外修改confdic
        self.__confdic[key] = value


    def Prepare(self,url,html,htmlcode):
        self.__confdic["url"] = url
        self.__confdic["html"] = html
        self.__confdic["HtmlCode"] = htmlcode
        self.Conf_update()

    def SaveHtml(self,content,encode):
        filepath = self.Get("HtmlFilePath")
        self.WriteNormal(filepath,content,encode)

    def ReadHtml(self):
        filepath = self.Get("HtmlFilePath")
        code = self.Get("HtmlCode")
        return self.ReadNormal(filepath,code)

    def Conf_update(self):
        # 更新本地confdic文件，主要是更新diclist
        self.Conf_write(self.__confdic)

    def OutPut(self,filename):
        targetfilepath = self.Get("ModelHome")+filename
        tempdiclist = []
        diclist = self.Get("diclist")
        for dic in diclist:
            if(dic["select"]==True):
                tempdiclist.append(dic)
        self.DicList_write(targetfilepath,tempdiclist)

def main():
    test = Model("Test")
    #print(test.GetConfDic())
    test.Prepare("url","html","utf-8")
    # diclist增加一个是否选择键值
    dic1 = {"title":"title1","content":"content1","select":True}
    dic2 = {"title":"title2","content":"content2","select":False}
    diclist = [dic1,dic2]
    test.Set("diclist",diclist)
    #print(test.GetConfDic())
    test.OutPut('test2.json')



if __name__=='__main__':
    main()