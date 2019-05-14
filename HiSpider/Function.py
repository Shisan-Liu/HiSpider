
def CheckAndMakeDir(path):
    className = "MakeDir_"
    # 检查并创建文件夹
    try:
        if(os.path.exists(path)==False):
            os.mkdir(path)
    except Exception as result:
        self.loclog.write("%s%s创建文件夹[%s][失败]:"%(self.classname,className,path,result))