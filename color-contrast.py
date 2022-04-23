import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import argparse
import pyfiglet
import wget
import re
import wcag_contrast_ratio as contrast
from matplotlib import colors
import matplotlib.pyplot as plt
#colors
def rgb_byte_to_float(colortuple):
     colorlist = list(colortuple)
     newlist = list()
     for number in colorlist:
        #print(number)
        try:
          newlist.append(int(number) / 255)
        except:
          newlist.append(number / 255)
        #Divide each element by 2
     newtuple  = tuple(newlist)
     if float(colorlist[0]) < 1.0 or float(colorlist[0]) == 1.0:
        return newtuple
     else:
        return colortuple
def colorcontrast_ratio(color1,color2):
    return contrast.rgb(color1, color2)
def convertor(color):
     #print(color[0:3])
     if color[0] == '#' and len(color) == 7:
        #print('need to convert hex to rgb' + color)
        hexvalue = color.lstrip('#')
        #print('RGB =', tuple(int(hexvalue[i:i+2], 16) for i in (0, 2, 4)))
        return tuple(int(hexvalue[i:i+2], 16) for i in (0, 2, 4))
     elif color[0:3] == 'rgb' or color[0:3] == 'RGB':
        #print('already in rgb')
        try:
          pattern = "((.*?))"
          substring = re.search(pattern, color).group(1)
          substring = '('+substring+')'
        except:
          substring = (0.0,0.0,0.0)
        return substring
        #print(substring)
     else:
        #print("else condition of converter")
        try:
          #print("trying for "+str(color))
          #print(colors.to_rgb(color))
          #print(type(colors.to_rgb(color)))
          #print(str(colors.to_rgb(color))+"converted from color name")
          return colors.to_rgb(color)
          #print(str(colors.to_rgb(color))+"converted from color name")
        except:
          #print("default")
          return (0.0, 0.0, 0.0)
          #print("default")
def curliremover(data):
    string = ""
    for x in data:
       string = string + x
       if x == "}":
         data = data[len(string):]
         return data
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
def result_putting(data,file_url,css_or_not):
   i = len(find_all(data,'{'))
   #print(str(i)+'length')
   k = 0
   ### by this as we got 1 element within the file with ADA ratio less then 4.5 , then the further checking will stop and css file get recorded
   for K in range(i):
      try:
        string = ""
        pattern = "{(.*?)}"
        substring = re.search(pattern, data).group(1)
      except:
        continue
      #print(substring)
      try:
        backcolor = re.search("background-color:(.*?);",substring).group(1)
        print("backcolor:"+backcolor)
      except:
        backcolor = "white"
      #print(str(backcolor).strip())
      try:
        frontcolor = re.search(" color:(.*?);",substring).group(1) or re.search(";color:(.*?);",substring).group(1)
      except:
        frontcolor = "black"
      #print(str(frontcolor).strip())
      data = curliremover(data)
      k = k+1
      #print('thee value of k is '+str(k))
      ## checking contrast ratio
      if backcolor == "white" and frontcolor == "black":
        #print('no need to check')
        x = 1
      else:
        #print('first converting to rgb')
        #print(convertor(backcolor))
        #print(rgb_byte_to_float(convertor(backcolor)))
        #print(colorcontrast_ratio((0.0, 0.0, 0.0),(1.0, 1.0, 1.0)))
        #print(rgb_byte_to_float(convertor(frontcolor)))
        #ratio = colorcontrast_ratio(rgb_byte_to_float(convertor(backcolor)),rgb_byte_to_float(convertor(frontcolor)))
        #print("contrast ratio of one of element is : "+str(ratio))
        try:
          print("within try of color contrast calcuation")
          ratio = colorcontrast_ratio(rgb_byte_to_float(convertor(backcolor)),rgb_byte_to_float(convertor(frontcolor)))
          print("front color: "+str(rgb_byte_to_float(convertor(frontcolor))))
          print(frontcolor)
          print("back color: "+str(rgb_byte_to_float(convertor(backcolor))))
          print(backcolor)
          print("contrast ratio of one of element is : "+str(ratio))
          #print(colorcontrast_ratio(rgb_byte_to_float(convertor(backcolor)),rgb_byte_to_float(convertor(frontcolor))))
          print("------------------------------------------------------------------------------------------------------------------------------------About the check ratio")
          if 1.0 < colorcontrast_ratio(rgb_byte_to_float(convertor(backcolor)),rgb_byte_to_float(convertor(frontcolor))) < 4.5:
             #print("For css file name "+css_file+"one of contrast ratio is: "+str(ratio))
             print("it should be greater then 4.5 for good ADA")
             file1 = open(target+'.txt','a')
             if css_or_not == 1:
               file1.write("\n For css file name "+file_url+" one of contrast ratio is: "+str(ratio)+'\n')
             elif css_or_not == 2:
               file1.write("\n For Main page "+file_url+" contrast ratio for one of the element within <style></style> is: "+str(ratio)+'\n')
               #print('we are in 2')
             elif css_or_not == 3:
               file1.write("\n For Main page: "+file_url+" contrast ratio for one of html tag  is: "+str(ratio)+'\n')
             file1.close()
             break
          else:
             print(" Contrast Ratio is good: "+str(colorcontrast_ratio(rgb_byte_to_float(convertor(backcolor)),rgb_byte_to_float(convertor(frontcolor)))))
        except:
          x = 2


ascii_banner = pyfiglet.figlet_format("Color contrast check!!")
print(ascii_banner)
print(f"{bcolors.pink}Author: Meenakshi Kharel , Viraj Vaishnav{bcolors.RESET}")
parser = argparse.ArgumentParser()
parser.add_argument("-t","--target",help="Target to scan...")
args = parser.parse_args()
target = args.target
#print(find_all('hello hello \r\n this is viraj hello this is viraj','hello'))
url = 'http://'+target
session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
html = session.get(url).content
# parse HTML using beautiful soup
soup = bs(html, "html.parser")
#print(soup)
#######---------------------------------------------------Searching for <style></style> content
try:
  data_between_style = re.search("<style>(.*?)</style>",str(soup).strip()).group(1)
except:
  data_between_style = re.search("<style>(.*?)</style>",str(soup).strip())
#print(data_between_style)
if data_between_style != None:
  result_putting(data_between_style,url,2)
########### ------------------------------------------------------ Above is for checking color contrast within <style></style>tag
####### -------------------------------------------------------- Searching for data between style=" and " or style=' and '
try:
  style_within_html_tag = re.search("style=\"(.*?)\"",str(soup).strip()).group(1) or re.search("style=\'(.*?)\'",str(soup).strip()).group(1)
except:
  style_within_html_tag = re.search("style=\"(.*?)\"",str(soup).strip()) or re.search("style=\'(.*?)\'",str(soup).strip())
print(style_within_html_tag)
if style_within_html_tag != None:
    result_putting("{"+style_within_html_tag+"}",url,3)
########---------------------------------------------------------Above is for checking color contrast within html tag
# get the CSS files
css_files = []

for css in soup.find_all("link"):
    if css.attrs.get("href"):
        # if the link tag has the 'href' attribute
        css_url = urljoin(url, css.attrs.get("href"))
        if css_url[-3:] == "css":
           css_files.append(css_url)
#print("Total CSS files in the page:", len(css_files))
with open("css_files.txt", "w") as f:
    for css_file in css_files:
        print(css_file, file=f)
        
#print("for css file: "+css_files)
print("----------------------------------------------------------------------------------------------------------")
for css_file in css_files:
   print("for css file : "+css_file)
   #filename = wget.download(css_file)
   cssfilereq = requests.get(css_file)
   #print('---------')
   data = str(cssfilereq.content).strip()
   #print(cssfilereq.content)
   #print('---------')
   result_putting(data,css_file,1)
   
        
        
         
