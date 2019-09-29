#!/bin/python
import base64
import time
import requests
import hashlib
from bs4 import BeautifulSoup
import re 
import os
import sys

#Value = "tryharder"
kv = ("\x74\x72\x79\x68\x61\x72\x64\x65\x72")
# Good Response
gRP = ("<Response [200]>")

#display my message to you all
print ("#############################################################")
print ("## This script is for the FC4me CTF to take OSCE           ##")
print ("## This will automatically get you all the required data   ##")
print ("## to register for the course. However you will only be    ##")
print ("## hurting yourself as you will not learn how to do it on  ##")
print ("## your own. This script was created to challenge me to    ##")
print ("## work on my python skills, it needs some error check     ##")
print ("## tweaks ..... Thanks mike				   ##")
print ("#############################################################")
print ""
print ("**** [ Getting Date from the server ] ****")
#Get date
urld = "http://www.fc4.me/"
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
gdate = requests.get(urld, headers=headers)
if str(gdate) == str(gRP):
	soupd = BeautifulSoup(gdate.content, 'html.parser')
	srvstr = re.findall(r'srvstr=\'(.*?)\'',str(soupd))[0]
	print "Todays Date: "
	print srvstr
else:
	sys.exit("**** [ Could not connect to " + urld + "Check your internet ] ****")
	
print ""
print ("**** [ Creating Security String ] ****")

#duplicate hashing function hexmd5(kv+srvstr)
try:
	m = hashlib.md5()
	m.update(kv+srvstr)
	kvhm = m.hexdigest()
	print "Key + Todays Date = SecurityString:"
	print kvhm;
	print ""
except:
	sys.exit("**** [ Could not create Security String ] **** ")


#Email address to register with: Cant be a free email account:
em = raw_input("Enter your email address, cant be a free one: ")

print ("**** [ Sending Email and SecurityString to server ] ****")
#Post data to fc4.me and get reg key and secret
url = "http://fc4.me/fc4me.php"
post_data = ("email="+em+"&securitystring="+kvhm+"\r")
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
fcp = requests.post(url, headers=headers, data=post_data)
if str(fcp) == str(gRP):
	soup = BeautifulSoup(fcp.content, 'html.parser')
	print ""
	print ("**** [ Decode Base 64 Block ] ****")
	basecode = soup.find('blockquote').get_text()
	dbase = base64.b64decode(basecode)
	print dbase
	rcode = re.findall(r'Code: (.*?) | ', str(dbase))[4]
	print ""
else:
	sys.exit("**** [ Could not connect to" + url + "Check your internet or check your email and security string] ****")


#Extracting shell code, creating a c shell to test shell code and compiling
try:
	print ("****[ Not done yet: Decode the shellcode ] ****")
	scod = re.findall(r'done! : (.*?)CC',str(dbase))[0]
	shc = (scod+"CC")
	print shc
except:
	sys.exit("**** [ Could not decode and retrieve shellcode ] ****")

try:
	print ""
	print ("****[ Writing C shell file ] ****")
	f = open("osce.c", "w+")
	f.write("#include<stdio.h>\r\n")
	f.write("#include<string.h>\r\n")
	f.write("unsigned char code[] = \""+shc+"\";\r\n")
	f.write("main()\r\n")
	f.write("{\r\n")
	f.write("printf(\"Shellcode Length:  %d\\n\", strlen(code));\r\n")
	f.write("int (*ret)() = (int(*)())code;\r\n")
	f.write("ret();\r\n")
	f.write("}\r\n")
	f.close()
except:
	sys.exit("**** [ Make sure you have permission to write to the directory ] ****")
try:
	print ""
	print (" **** [ OSCE.c Created ] **** ")
	f = open ("osce.c", "r")
	if f.mode == 'r':
		ccode = f.read()
		print ccode
	else:
		print ("**** [ Could not read the file osce.c ] ****")
except:
	sys.exit("**** [ Could not read the file osce.c make sure it exists ] ****")
try:
	print ""
	print ("**** [ Compiling osce.c: Ignore Warnings ] ****")
	cmd = ("gcc osce.c -o osce -fno-stack-protector -z execstack -no-pie")
	os.system(cmd)
	print ""
except: 
	sys.exit("**** [ Compiling failed, check permissions and that you have a compiler installed ] ****")
try:
	print ("**** [ Running gnu debugger aginst OSCE to find key ] ****")
	#Interacting with gdb to debug and get key
	print ""
	print ("**** [Extracting the Key ] ****")
	dcmd = ("gdb -q -x ctpgdb.py >> key.txt")
	os.system(dcmd)
	time.sleep(5)
	f = open("key.txt", "r")
	if f.mode == 'r':
		contents = f.read()
		keyme = re.findall(r':	\"(.*?)\"', str(contents))
		if len(keyme[4]) != 128:
			print "error"
		else:
			print "Key is proper length"
	f.close()
except:
	sys.exit("**** [ Make sure ctpgdb.py is in same directory and executable, make sure key.txt exists ] ****")
try:
	print ""
	print ("**** [ Registration inforamtion for OSCE ] ****")
	print ("Email address: "+em+"")
	print ("Registration Code: "+rcode+"")
	print ("128 Byte Secret Key: "+keyme[4]+"")
except:
	sys.exit("**** [ Try harder!! ] ****")
#Clean up
cdel = ("rm -Rf osce.c key.txt")
os.system(cdel)
