#coding=utf-8
import pexpect

#提示符
PROMPT=['#','>>>',',','\$']

def send_command(child,cmd):
	child.sendline(cmd)
	child.expect(PROMPT)#匹配提示符
	print child.before#before获取命令执行的结果

def connect(user,host,password):
        ssh_newkey='Are you sure you want to continue connecting'
        connStr='ssh '+user+'@'+host
        child=pexpect.spawn(connStr)#执行程序，并获得程序操作句柄
        ret=child.expect([pexpect.TIMEOUT,ssh_newkey,'[P|p]assword:'])#匹配关键字，返回几就表示匹配到了几，从０开始
        if ret==0:
                print '[-] Error Connecting'
                return
        if ret==1:
                child.sendline('yes')
                ret=child.expect([pexpect.TIMEOUT,'[P|p]assword:'])
        if ret==0:
                print '[-] Error Connecting'
                return
        child.sendline(password)
        child.expect(PROMPT)#匹配提示符
        return child
#给可用的地址，用户，密码等，并调用
def main():
	host=''
	user=''
	password=''
	child=connect(user,host,password)
	while(True):
		x=raw_input("请输入你的命令")
		if x=='exit()':
			return
		send_command(child, x)
#程序入口
if __name__=='__main__':
	main()	




























