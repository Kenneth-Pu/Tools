#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import socket
import optparse
import threading
import nmap

#调用nmap
def nmapScan(targetHost,targetPort):
    targetIP=socket.gethostbyname(targetHost)
    nmScan=nmap.PortScanner()
    nmScan.scan(targetIP,targetPort)
    state=nmScan[targetIP]['tcp'][int(targetPort)]['state']
    print "[*]" + targetHost + "tcp/" +targetPort+" "+state

#第一步 从用户获得主机名和端口
def maim():
    parser=optparse.OptionParser('usage %prog -H'+'<target host> -p <target port>')
    parser.add_option('-H',dest='targetHost',type='string',help='输入目标地址')
    parser.add_option('-P',dest='targetPort',type='string',help='输入目标端口')
    (options,args)=parser.parse_args()
    targetHost=options.targetHost
    targetPorts=str(options.targetPort).split(',')
    print targetHost,targetPorts
    if (targetHost==None) | ((targetPorts[0]==None)):
        print "请输入正确的格式"
        exit(0)
    for targetPort in targetPorts:
        nmapScan(targetHost,targetPort)
if __name__ == '__main__':
    maim()





