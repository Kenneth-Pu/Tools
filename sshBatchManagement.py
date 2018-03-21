#coding=utf-8
import pexpect.pxssh
import optparse

botNet=[]
class Client:
    def __init__(self,targetHost,user,password):
        self.targetHost=targetHost
        self.user=user
        self.password=password
        self.session=self.connect()
    def connect(self):
        try:
            s=pexpect.pxssh.pxssh()
            s.login(self.targetHost,self.user,self.password,login_timeout=100)
            return s
        except Exception ,e:
            print e
            print '%s连接失败' % self.targetHost
    def send_command(self,cmd):
            self.session.sendline(cmd)
            self.session.prompt()
            return self.session.before
#ｃｍｄ
def botnetCommand(command):
    for c in botNet:
        output=c.send_command(command)
        print '[*] output from'+c.targetHost
        print '[+]' +output+'\n'

#创建client,并且加入列表
def addClient(targetHost,user,password):
    client=Client(targetHost,user,password)
    botNet.append(client)

def main():
    parse=optparse.OptionParser('格式　-F<文件名>')
    parse.add_option('-F',dest='messageFile',type='string',help='连接参数文件')
    (options,args)=parse.parse_args()
    fileName=options.messageFile
    print fileName
    file=open(fileName,'r')
    for line in file.readlines():
        mass=line.strip('\n')
        masslist=mass.split(' ')
        addClient(masslist[0],masslist[1],masslist[2])
        while True:
            cmd = raw_input('请输入命令：')
            botnetCommand(cmd)

if __name__ == '__main__':
    main()
