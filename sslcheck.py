import requests
import argparse
import pyfiglet
import socket
import ssl
import datetime
import json
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import re
#colors
class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR
    B = "\033[0;34;40m" # Blue
    orange='\033[43m' 
    purple='\033[45m'
    cyan='\033[46m'
    lightgrey='\033[47m'
    lightgrey='\033[37m'
    darkgrey='\033[90m'
    lightred='\033[91m'
    pink='\033[95m'
def ssl_information(hostname):
    ssl_dateformat = r'%b %d %H:%M:%S %Y %Z'

    context = ssl.create_default_context()
    context.check_hostname = False

    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=hostname,
    )
    # 5 second timeout
    conn.settimeout(5.0)

    conn.connect((hostname, 443))
    ssl_info = conn.getpeercert()
    print(ssl_info)
    with open(hostname+".json", "w") as write_file:
       json.dump(ssl_info, write_file, indent=4)
    # Python datetime object
    #return datetime.datetime.strptime(ssl_info['notAfter'], ssl_dateformat)
def check_ssl(url,domain):
    result = "nothing"
    try:
        req = requests.get(url,allow_redirects=True, verify=True)
        print(url + ' has a valid SSL certificate!')
        result = 'true'
        ssl_information(domain)
    except requests.exceptions.SSLError:
        print(url + ' has Invalid SSL certificate!')
        result = 'false'
    #return result
    ## writing output to file
    file1 = open(domain+".txt", "a") 
    file1.write(result+"\n")
    file1.close()
    print("sslcheck result: "+result)
    #### new lines added for verfiy_all_links
    if result == 'true':
       verify_all_links('https://'+domain,domain)
    else:
       verify_all_links('http://'+target,target)
def verify_all_links(url,target):
     links = []
     session = requests.Session()
     # set the User-agent as a regular browser
     session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
     # get the HTML content
     html = session.get(url).content
     soup = bs(html, "html.parser")
     for link in soup.findAll('a'):
        links.append(link.get('href'))
     #print(str(links))
     all_http_links = list()
     for link in links:
        #print(link)
        #print(type(link))
        #print(link[0:5])
        if link != None and len(link) > 5 and link[0:5] == 'https':
            print('ok '+'for '+link)
        else:
            if link != None and len(link) > 5 and link[0:5] == 'http:':
              all_http_links.append(link)
            else:
             print('url skipped , no need to check ....')
     if len(all_http_links) > 0:
              f = open(target+".httplinks.txt",'w')
              f.write("We found some urls which are hosted using http protocol: "+'\n')
              f.close()
              for link in all_http_links:
                 f = open(target+".httplinks.txt",'a')
                 f.write(link+'\n')
                 f.close()
     else:
              f = open(target+".httplinks.txt",'a')
            #   f.write("All urls within the page are hosted using https protocol : "+'\n')
              f.close()
              




################  main
ascii_banner = pyfiglet.figlet_format("SSL Checker !!")
print(ascii_banner)
print(f"{bcolors.pink}Author: Meenakshi Kharel , Viraj Vaishnav{bcolors.RESET}")
parser = argparse.ArgumentParser()
parser.add_argument("-t","--target",help="Target to scan...")
args = parser.parse_args()
target = args.target
check_ssl('https://'+target,target)