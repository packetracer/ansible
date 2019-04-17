#!/usr/bin/python
import subprocess
import sys
import cgi
import datetime
import re
import requests

validMac = False
ERROR = False

form = cgi.FieldStorage()
user = "READONLY_USER_HERE"
pwd = "PASSWORD"
OUI = form.getvalue('OUI')
host = form.getvalue('HOST')

def formatOUI(OUI):
        ot=OUI[0:2]
        tf=OUI[2:4]
        fs=OUI[5:7]
        fmac = ot+":"+tf+":"+fs+":00:00:00"
        return fmac

fOUI = formatOUI(OUI)
webCmd = "show ip arp | i {}".format(OUI[0:7])

def printHeader():
        print "Content-type: text/html"
        print ""
        print "<html><head>"
        print "<title>OUI Finder</title></head><body>"
        print "<br />Time run: " + str(datetime.datetime.now()) + "<br>"


def checkInput():
        pattern = re.compile('[a-fA-F0-9]{4}.[a-fA-F0-9]{2}')
        if re.match(pattern,OUI[0:7]):
                return True
        else:
                return False

def sanitize(outp):
        item=[]
        outp = outp.split('# STATS ')[0]
        outp = outp.split(' * ')
        del outp[0]
        print "<BR>"
        item = []
        for i in outp:
                entry = []
                i = i.replace('changed=False','')
                if "Internet" not in i:
                        entry.append(i.split(' ')[0])
                else:
                        entry.append(i.split(' ')[0])
                        i = i.split(' Internet  ')
                        del i[0]
                        for j in i:
                                j = j.split(' ')
                                j = [k for k in j if k]
                                del j[1]
                                del j[2]
                                entry.append(j)
                item.append(entry)
        return item

def displaySanitized(hosts):
        totHosts = 0
        for i in hosts:
                if len(i)>1:
                        totHosts+=(len(i)-1)
        print "<CENTER>"
        print "Number of hosts found: " + str(totHosts)
        print "<TABLE border='1' cellpadding='10'> "
        for item in hosts:
                if len(item) == 1:
                        print "<TR><TH colspan='3'>"
                        print item[0]
                        print "</TH></TR>"
                        print "<TR><TH>IP</TH><TH>MAC</TH><TH>VLAN</TH>"
                        print "<TR><TD colspan='3'>No hosts found</TD></TR>"
                else:
                        print "<TR><TH colspan='3'>"
                        print item[0]
                        print "</TH></TR>"
                        print "<TR><TH>IP</TH><TH>MAC</TH><TH>VLAN</TH>"

                        for i in range(1,len(item)):
                                print "<TR><TD>"
                                print item[i][0]
                                print "</TD><TD>"
                                print item[i][1]
                                print "</TD><TD>"
                                print item[i][2]
                                print "</TD></TR>"

        print "</TABLE>"


def executeCmd(host):
        cmd = """ansible-playbook /ansible/plays/show_cmd.yml --limit '"""+host+"""' -e 'user="{0}" pass="{1}" cmd="{2}"' |  sed 's/\\\\n/\\n/g'""".format(user,pwd,webCmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        outp = str(p.communicate()[0])
        if 'Authentication failed.' in outp:
                        print "<CENTER><H1>***ERROR!***<br>Authentication failed.</H1><h3>Check credentials</h3></CENTER>"
        displaySanitized(sanitize(outp))

def lookup(OUI):
        MAC_URL = 'http://macvendors.co/api/%s'
        r = requests.get(MAC_URL % OUI)
        print "<CENTER><h3>Vendor Name: "+(r.json()['result']['company'])+"</h3></CENTER>"

printHeader()
validMac = checkInput()

if validMac == False:
        print "<CENTER><h3>{} OUI not formatted correctly, please use xxxx.xx (Cisco format).</h3></CENTER>".format(OUI)
else:
        try:
                lookup(fOUI)
        except:
                ERROR = True
                print "<CENTER>OUI not found in database!<br>Check and try again</CENTER>"
        if ERROR == False:
                executeCmd(host)
