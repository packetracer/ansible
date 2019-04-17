#!/usr/bin/python
import subprocess
import sys
import cgi
import datetime
form = cgi.FieldStorage()
devName = form.getvalue('devName')
webCmd = form.getvalue('webCmd')
user = form.getvalue('user')
pwd = form.getvalue('pwd')

def printHeader():
        print "Content-type: text/html"
        print ""
        print "<html><head>"
        print "<title>Show Command</title></head><body>"
        print "<h3>Target Host: {}</h3>".format(devName)
        print "<br />Command run: " + webCmd
        print "<br />Time run: " + str(datetime.datetime.now()) + "<br>"


def checkInput():
        if '.' in devName:
                cmd = "python ip-to-host.py {}".format(devName)
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                host = p.communicate()[0]
                return host.strip('\n')
        else:
                cmd = "cat /etc/ansible/hosts"
                p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                cmd = p.communicate()[0]
                cmd = cmd.split('\n')
                for lines in cmd:
                        if devName in lines:
                                return devName
                return "Host not found"

def executeCmd(host):
        cmd = """ansible-playbook /ansible/plays/show_cmd.yml --limit '"""+host+"""' -e 'user="{0}" pass="{1}" cmd="{2}"'""".format(user,pwd,webCmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        outp = str(p.communicate()[0])
        if 'Authentication failed.' in outp:
                        print "<CENTER><H1>***ERROR!***<br>Authentication failed.</H1><h3>Check credentials</h3></CENTER>"
                        return

        sanep = outp.split('----------------------------------------------\n')[1].split('# STAT')[0].replace('\n\n','')

        for lines in sanep.split('\n'):
                if 'Building' not in lines:
                        print lines+'<br>'

#-- START
printHeader()
host = checkInput()

if host == "Host not found":
        print "{} not in hosts file, command rejected.".format(devName)
else:
        executeCmd(host)
