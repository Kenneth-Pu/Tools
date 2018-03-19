# _*_ coding:utf-8 _*_
import optparse
import socket
import threading

#第三步
screenLock=threading.Semaphore(value=1)
def connScan(targetHost,targetPost):
    try:
        connSock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        connSock.connect((targetHost,targetPost))
        connSock.send('ViolentPython\r\n')
        results=connSock.recv(100)
        screenLock.acquire()
        print "[*]%s/tcp是打开的" %targetPost
        print '[*]'+str(results)
    except:
        screenLock.acquire()
        #print '[*]%s/tcp是关闭的' %targetPost
    finally:
        screenLock.release()
        connSock.close()

#第二步
def portScan(targetHost,targetPosts):
    try:
        targetIP=socket.gethostbyname(targetHost)
    except:
        print "无效网址 %s" %targetHost
        return
    try:
        targetName=socket.gethostbyaddr(targetIP)
        print "主机名是 %s" %targetName
    except:
        print "扫描ip地址 %s" %targetIP
    socket.setdefaulttimeout(1)
    for targetPost in targetPosts:
        #print "扫描端口 %s" %targetPost
        t=threading.Thread(target=connScan,args=(targetHost,int(targetPost)))
        t.start()
#第一步从命令行接收参数
def maim():
    num=''
    for i in range(1000):
        num+=(str(i)+',')
    num=num[:-1]
    parser=optparse.OptionParser("格式是 python TCPscan.py -H127.0.0.1 -P8080")
    parser.add_option('-H',dest='targetHost',type='string',help='这是地址')
    parser.add_option('-P',dest='targetPost',type='string',help='这是端口',default=num)
    (options,args)=parser.parse_args()
    targetHost=options.targetHost
    targetPosts=str(options.targetPost).split(',')
    if (targetHost==None) | (targetPosts[0]==None):
        print '[-]你需要一个地址和至少一个端口'
        exit(0)
    portScan(targetHost,targetPosts)


if __name__ == '__main__':
    maim()
