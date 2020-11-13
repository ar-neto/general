import os
import requests
import io
import unicodedata

def run(com): #runs the command
    c = str(os.system(com))

def runwhois(url):
    os.chdir("C:\\sample_directory\\tools\\WhoIs\\") #change to whois instalation directory; input here the whois installation directory
    c= str(os.system("whois "+url))#crun whois

print("paste the desired URL")
url= input() #the asset's URL is placed here

run("C:\\instalation_path\\sublist3r.py -d "+url+" -v") #run sublister; place its absolute instalation path
run("\"C:\\instalation_path\\nmap.exe\" -T4 -A -v -sS "+url) #runs nmap
run("nmap --script vuln "+url)
run("nslookup "+url) #executes the nslookup command
run("tracert "+url) #executes the tracert command
run("ping "+url) #executes 4 ping requests
run("nbtstat -A "+url) #enumerates the targets' NETBIOS
runwhois(url)