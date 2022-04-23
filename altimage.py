import requests
import argparse
import pyfiglet
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
def find_all(a_string, sub):
    result = []
    k = 0
    while k < len(a_string):
        k = a_string.find(sub, k)
        if k == -1:
            return result
        else:
            result.append(k)
            k += 1 #change to k += len(sub) to not search overlapping results
    return result
    

ascii_banner = pyfiglet.figlet_format("Alt text check!!")
print(ascii_banner)
print(f"{bcolors.pink}Author: Meenakshi Kharel , Viraj Vaishnav{bcolors.RESET}")
parser = argparse.ArgumentParser()
parser.add_argument("-t","--target",help="Target to scan...")
args = parser.parse_args()
target = args.target
#print(find_all('hello hello \r\n this is viraj hello this is viraj','hello'))
url = 'http://'+target
r = requests.get(url, allow_redirects=True)
#print(r.content)
data = str(r.content).strip()
#print(data)
li = find_all(str(r.content),'<img')
result = [] 
for i in li: 
    if i not in result: 
        result.append(i)
#print(find_all(str(r.content),'<img'))
for i in result:
  string = ""
  for x in str(r.content)[i:-1]:
    string = string + x
    if x == '>':
      result = string
      print(string + '\n')
      if 'alt=' in string:
        #print('yes alt text is there')
        if 'alt=""' in string:
          print('\n No alt text found \n')
          result += '\n No alt text found \n'
          f = open(target+".txt","a")
          f.write(result + '\n')
          f.close()
          break
        else: 
          print('Yes alt text is there \n')
      else:
        print('No alt text found \n')
        result += 'No alt text found \n'
        f = open(target+".txt","a")
        f.write(result +'\n')
        f.close()
        break
    