from flask import Flask, render_template, request, make_response, jsonify
import os
import pdfkit
from werkzeug.wrappers import response
app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def home():
#    if(request.method == 'POST'):
#       print(request.form.getlist('check'))
#       return 'Scan in Process'
#    return render_template('home.html')

s1a = "SSL Certificate Compliance Check Not Performed"
s1b = ""
s1c = ""
s2a = "Cookie Checker Scan Not Performed"
s3a = "ADA Compliance Check Not Performed"
s3aa = ""
s3b = ""
s3c = ""
s3cc = ""

def scan1a(target):
    f = open(target+'.txt','w')
    #f.write('#sslcheck\n')
    f.close()
    os.system('python3 sslcheck.py -t '+str(target))
    #print('the value of x is '+x)

def scan2a(target):
    f = open(target+'.txt','w')
    #f.write('#httponly\n')
    f.close()
    os.system('python3 httponly.py -t '+str(target))
    #print('the value of x is '+x) 

def scan3a(target):
    f = open(target+'.txt','w')
   #  f.write('#altimage ' + '\n')
    f.close()
    os.system('python3 altimage.py -t '+str(target))
    #print('the value of x is '+x)
    
def scan3b(target):
    f = open(target+'.txt','w')
   #  f.write('#tabindex \n')
    f.close()
    os.system('python3 tabindex.py -t '+str(target))
    #print('the value of x is '+x)
    
def scan3c(target):
    f = open(target+'.txt','w')
   #  f.write('#colorcontrast \n')
    f.close()
    os.system('python3 color-contrast.py -t '+str(target))
    #print('the value of x is '+x)

@app.route('/', methods=['GET', 'POST'])
def index():
   if(request.method == 'POST'):
      link = request.form.get('link') 
      print(link)
      # print (type(link))
      scan_values = request.form.getlist('check')
      # print(scan_values)
      for i in scan_values:
         print(i)
      
      for val in scan_values:
         if(val == '1'):
            global s1a
            s1a = ""
            scan1a(link)
            f = open(link+'.txt','r')
            val = f.read()
            print('val = ' + val )
            if val == 'true\n':
               s1a = "<h4>" + link + " has a VALID SSL Certificate. </h4> \n"
            else:
               s1a = "<h4> The scanned website has a INVALID SSL Certificate. </h4> \n"
            f.close() 
            global s1b
            f = open(link + '.json', 'r')
            s1b = f.read()
            f.close()

            global s1c
            f = open(link + '.httplinks.txt', 'r')
            s1c = f.read()
            if s1c.isspace() or len(s1c) == 0:
               s1c = '<h4> All links in ' + link + ' have VALID SSL Certificates </h4> \n'
               s1a += '\n <h4> All links in ' + link + ' have VALID SSL Certificates </h4> \n'
            else:
               s1a += '\n <h4> We have found some urls which are hosted using http protocol. </h4> \n'
            s1a = s1a.replace('\n', '<br>')
            s1b = s1b.replace('\n', '<br>')
            s1c = s1c.replace('\n', '<br>')
         elif(val == '2'):
            global s2a
            s2a = ""
            scan2a(link)
            f = open(link+'.txt','r')
            s2a = f.read()
            s2a = s2a.replace('\n', '<br>')
            f.close()
         elif(val == '3'):
            global s3a
            global s3aa
            s3a = ""
            scan3a(link)
            f = open(link+'.txt','r')
            s3a = f.read()
            print('s3a = ' + s3a)
            if s3a.isspace() or len(s3a) == 0:
               s3a = '<h4> All images in ' + link + ' have alt text. </h4>\n'
               s3aa = s3a
            else:
               temp = s3a
               s3a = '<h4> We have found some images in ' + link + ' which DO NOT have alt text. </h4> \n'
               s3aa = s3a + '\n' + temp + '\n' + '\n'
            s3a = s3a.replace('\n', '<br>')
            s3aa = s3aa.replace('\n', '<br>')
            f.close()

            global s3b
            scan3b(link)
            f = open(link+'.txt','r')
            s3b = f.read()
            s3b = s3b.replace('\n', '<br>')
            f.close()

            global s3c
            global s3cc
            scan3c(link)
            f = open(link+'.txt','r')
            s3c = f.read()
            if s3c.isspace()  or len(s3c) == 0:
               s3c = '<h4>The color contrast in ' + link + ' is correct. </h4> \n'
               s3cc = s3c
            else:
               temp = s3c
               s3c = '<h4> We have found that the color contrast ratio for some elements in ' + link + ' is less than 4.5:1 </h4>'
               s3cc = s3c + '\n' + temp + '\n' + '\n'
            s3c = s3c.replace('\n', '<br>')
            s3cc = s3cc.replace('\n', '<br>')
            f.close()
      
      try:
         os.system('rm -rf '+link+'.txt')  # for linux
         os.system('rm -rf '+link+'.json')  # for linux
         os.system('rm -rf '+link+'httplinks.txt')  # for linux
      except:
         os.system('del /f '+link+'.txt')  # for windows
         os.system('del /f '+link+'.json')  # for windows
         os.system('del /f '+link+'httplinks.txt')  # for windows
      return render_template('report.html', s1a = s1a, s2a=s2a, s3a=s3a, s3b=s3b, s3c=s3c)      

   return render_template('index.html')


@app.route('/summary')
def pdf_template():
   rendered = render_template('summary.html', s1a = s1a, s2a=s2a, s3a=s3a, s3b=s3b, s3c=s3c)
   css = ['static/assets/css/templatemo-chain-app-dev.css']
   pdf = pdfkit.from_string(rendered, False, css=css)
   
   response = make_response(pdf)
   response.headers['Content-Type'] = 'application/pdf'
   try:
      response.headers['Content-Disposition'] = 'attachment; filename = summary.pdf'
      return response
   except:
      return '<h4 style="text-align: center;"> Size of the file is too big too download </h4>'

@app.route('/details')
def pdf_template2():
   rendered = render_template('details.html',  s1a = s1a, s1b=s1b, s1c = s1c, s2a = s2a, s3a = s3aa, s3b = s3b, s3c = s3cc)
   css = ['static/assets/css/templatemo-chain-app-dev.css']
   pdf = pdfkit.from_string(rendered, False, css=css)
   
   response = make_response(pdf)
   response.headers['Content-Type'] = 'application/pdf'
   try:
      response.headers['Content-Disposition'] = 'attachment; filename = details.pdf'
      return response
   except:
      return '<h4 style="text-align: center;"> Size of the file is too big to download </h4>'
   

@app.route('/ssl')
def ssl_readmore():
   return render_template('ssl.html', s1a = s1a, s1b=s1b, s1c = s1c) 

@app.route('/cookie')
def cookie_readmore():
   return render_template('cookie.html', s2a = s2a) 

@app.route('/ada')
def ada_readmore():
   return render_template('ada.html', s3a = s3aa, s3b = s3b, s3c = s3cc) 


if __name__ == "__main__":
    app.run(debug=True, port=8000)
