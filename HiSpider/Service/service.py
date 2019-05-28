
# 定时抓取，邮件提醒，等功能放到服务器
# 客户端发送请求获取服务器数据即可实现离线抓取

# 需要身份验证，如果后期收费的话还要根据ID进行一些操作
import socket,time,threading,json

class Service(object):
    def __init__(self, *args, **kwargs):
        self.port = 9999
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', self.port))
        s.listen(5)
        print('Waiting for connection...')
        while True:
            # 可以有很多个线程监听多个端口，处理不同的事件
            # 接受一个新连接:
            sock, addr = s.accept()
            # 创建新线程来处理TCP连接:
            t = threading.Thread(target=tcplink, args=(sock, addr))
            t.start()
        return super().__init__(*args, **kwargs)



    def tcplink(sock, addr):

        print('Accept new connection from %s:%s...' % addr)

        dic = json.loads(sock.recv(1024))
        username = dic["user"]
        passwd = dic["passwd"]

        if(username=='1234' and passwd=='1234'):
            sock.send(('Hello, %s!' % username).encode('utf-8'))
        else:
            sock.send(('False, %s!' % username).encode('utf-8'))

        sock.close()
        print('Connection from %s:%s closed.' % addr)


def main():
    print()

if __name__=="__main__":
    main()
