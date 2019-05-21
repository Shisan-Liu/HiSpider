import urllib.request
import chardet
class urlrequest(object):
    def __init__(self):
        self.code = ''
    def GetHtml(self,url):
        response = urllib.request.urlopen(url)
        # read（）获取的是二进制数据
        bytesres = response.read()
        # 查码
        self.code = chardet.detect(bytesres)["encoding"]
        print(self.code)
        # 解码
        souce = bytesres.decode(self.code)
        # 转码
        final = souce.encode("utf-8")
        print(chardet.detect(final)["encoding"])
        return final.decode("utf-8")
