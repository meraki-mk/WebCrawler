import argparse
import pyfiglet
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import re
import wcag_contrast_ratio as contrast
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
pii_value = ""
global response_from_server
global URL_TARGET
def check_cookie_consent(response,url):
   print(response.content)
   x = True
   ## checking within script tags
   try:
     data_between_function = re.search("window.cookieconsent.initialise\({(.*?)}\);",str(response_from_server.content).strip()).group(1)
   except:
     data_between_function = re.search("window.cookieconsent.initialise\({(.*?)}\);",str(response_from_server.content).strip())
   #print(data_between_function)
   if data_between_function != None and len(data_between_function) > 1:
      #print("cookie consent is there")
      #print("window.cookieconsent.initialise({"+data_between_function+"});")
      x = False
   else:
      #print("No consent")
      #print(data_between_function)
      x = True
   ## checking cookie consent for within js files
   if x:
     # get the JavaScript files
     script_files = []
     session = requests.Session()
     # set the User-agent as a regular browser
     session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
     # get the HTML content
     html = session.get(url).content
     soup = bs(html, "html.parser")

     for script in soup.find_all("script"):
       if script.attrs.get("src"):
         # if the tag has the attribute 'src'
         script_url = urljoin(url, script.attrs.get("src"))
         script_files.append(script_url)
     for item in script_files:
         f = open('js.txt','a')
         f.write(item)
         f.close()
         r = requests.Session()
         jsrs = r.get(item)
         try:
           data_between_function = re.search("window.cookieconsent.initialise\({(.*?)}\);",str(jsrs.content).strip()).group(1)
         except:
           data_between_function = re.search("window.cookieconsent.initialise\({(.*?)}\);",str(jsrs.content).strip())
         if data_between_function != None and len(data_between_function) > 1:
            #print("cookie consent is there")
            #print("window.cookieconsent.initialise({"+data_between_function+"});")
            x = False
            break
         else:
            #print("No consent")
            #print(data_between_function)
            x = True
   if x:
    return False
   else:
    return True
def check_ssl(url):
    try:
        req = requests.get(url, verify=True)
        return True
    except requests.exceptions.SSLError:
        return False
def has_http_only(cookie):
    extra_args = cookie.__dict__.get('_rest')
    if extra_args:
        for key in extra_args.keys():
            if key.lower() == 'httponly':
                return True

    return False
## checking for any PII or credentials leakage
def pii(cookie):
    extra_args = cookie.__dict__.get('_rest')
    if extra_args:
        for key in extra_args.keys():
            global pii_value
            print('this is key===>>> '+key)
            if key.lower() == 'username':
               pii_value = "username"
               return True
            elif key.lower() == 'password':
                pii_value = "password"
                return True
            elif key.lower() == 'email':
                pii_value = "email"
                return True
            elif key.lower() == 'nid':
                pii_value = "mail"
                return True
            else:
                return False

    #return False
ascii_banner = pyfiglet.figlet_format("HTTPOnly Flag Check !!")
print(ascii_banner)
print(f"{bcolors.pink}Author: Meenakshi Kharel , Viraj Vaishnav{bcolors.RESET}")
parser = argparse.ArgumentParser()
parser.add_argument("-t","--target",help="Target to scan...")
args = parser.parse_args()
target = args.target
if check_ssl('https://'+target):
   #r = requests.post('https://'+target)
   URL_TARGET = 'https://'+target
   session = requests.Session()
   r = session.get('https://'+target)
   result = ""
   response_from_server = r

   if has_http_only(r.cookies):
      print('-->> '+target+' has httponly flag set to true \n')
      result = '<h4>' + target + ' has HttpOnly Flag set to True </h4>\n'
   else:
      print('-->> '+target+' has httponly flag set to False \n')
      result += '<h4> '+ target + ' has HttpOnly Flag set to False </h4> \n'

   if pii(r.cookies) is not None:
      print('-->> '+target+' contains a cookie which might leaking some Personally identifiable information (PII) '+ pii_value) + '\n'
      result += '\n <h4> '+target+' contains a cookie which might leaking some Personally identifiable information (PII) '+ pii_value + ' </h4> \n'
   else:
      print(target+' contains no PII')
      result = result+'\n <h4> ' +target+' contains no Personally identifiable information (PII) </h4> \n'
      #print(pii(r.cookies))
   f  = open(target+'.txt','a')
   f.write(result+'\n')
   f.close()
else:
   result = ""
   URL_TARGET = 'http://'+target
   r = requests.get('http://'+target)
   response_from_server = r
   if has_http_only(r.cookies):
      print('-->> '+target+' has httponly flag set to true \n')
      result = '<h4>' + target + ' has httponly flag set to true </h4> \n'
   else:
      print('-->> '+target+' has httponly flag set to False \n')
      result = '<h4>' + target + ' has httponly flag set to False </h4>\n'
   if pii(r.cookies):
      print('-->> '+ target + ' contains a cookie which might leaking some Personally identifiable information (PII) '+ pii_value) + '\n'
      result += target + ' contains a cookie which might leaking some Personally identifiable information (PII) '+ pii_value + '\n'
   else:
      print('-->> '+target+' contains no Personally identifiable information (PII) \n')
      result +=  '<h4>' + target +' contains no Personally identifiable information (PII) </h4> \n'
   f  = open(target+'.txt','a')
   f.write(result+'\n')
   f.close()
   
## chceking cookie consent , below is the boolean to check whether the cookie consent is there or not  
consent = check_cookie_consent(response_from_server,URL_TARGET)
if consent:
  f = open(target+'.txt','a')
  f.write('<h4> Cookie Consent is there. \n' + target + ' asks for the permission before storing the cookies </h4> \n')
  print('Cookie Consent is there. \n' + target + ' asks for the permission before storing the cookies \n')
  f.close()
else:
  f = open(target+'.txt','a')
  f.write('<h4> No Cookie Consent is there. \n' + target + ' does not ask for the permission before storing the cookies </h4> \n')
  print('No Cookie Consent is there. \n' + target + ' does not ask for the permission before storing the cookies \n')
  f.close()