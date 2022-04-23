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
    

ascii_banner = pyfiglet.figlet_format("TabIndex check!!")
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
li = find_all(str(r.content),'tabindex=')
#print(find_all(str(r.content),'<img'))
value = False
for i in li:
  print(data[i+9:i+13])
  if data[i+9:i+11] == '"-' or data[i+9:i+12] == '"0"' or data[i+9] == 0 or data[i+9] == -1:
    print('Tabindex value is correct \n')
    file1 = open(target+'.txt','a')
    file1.write('<h4> Tabindex value of '+ target + 'is correct. </h4> \n')
    file1.close()
  else:
     print(data[i:i+15]+"is found ")
     value = True
file1 = open(target+'.txt','a')
file1.write('<h4> We have discovered some tabindex with value greater then 1 in '+ target + '. Please check the source code. </h4> \n')
file1.close()
    
