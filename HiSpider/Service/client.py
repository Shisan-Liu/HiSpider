
# 客户端封装一些操作，比如拉取服务器数据，创建一个抓取队列，刷新 服务器状态等
# 类似于数据库操作，更复杂
import socket,json

class Client(object):
    def __init__(self, *args, **kwargs):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 9999))

        username = "1234"
        passwd = "12345"
        dic = {"user":username,"passwd":passwd}
        list = [dic]
        json_str = json.dumps(dic)

        s.send(json_str.encode("utf-8"))

        print(s.recv(1024).decode('utf-8'))

        s.send(b'exit')
        s.close()
        return super().__init__(*args, **kwargs)




def main():
    print()

if __name__=="__main__":
    main()
