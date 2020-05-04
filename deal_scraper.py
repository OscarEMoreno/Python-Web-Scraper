#Web scraper
#Oscar M. 2020

#from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders

description=[] #store descriptions of the product
brands = [] # store brands

def sendEmail(): 
    sender = "@"
    mypass = ""
    receiver = sender

    body = "Here are the deals"
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Date'] = formatdate(localtime = True)
    msg['Subject'] = "Deals"
    msg.attach(MIMEText(body))

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open("Deals.xlsx", "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="Deals.xlsx"')
    msg.attach(part)

    # Start connection
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender,mypass)
    try:
        server.sendmail(sender,receiver, msg.as_string())
        print ('Email sent')
    except:
        print ('Error sending mail')
    server.quit()

###First attempt. Needs selenium
##url_1 = 'https://www.cupones.es/'
##page = requests.get(url_1)
##soup = BeautifulSoup(page.content, 'html.parser')
##voucher = []
##my_elems = soup.find_all(class_='resultList-container resultList-container--primary')
##for element in my_elems:
##    for id_page in element.find_all(True,{'id':True}):
##        voucher.append(id_page.get('id')[-5:])
##print(voucher)
##for voucher_code in voucher:
##    url_2 = url_1 +"#show="+ voucher_code
##    print(url_2)
##url_2 = 'https://www.cupones.es/#show=71765' 
##page = requests.get(url_2)
##soup = BeautifulSoup(page.content, 'html.parser')
##my_elems = soup.find_all(class_='titleMain')
##for element in my_elems:
##    print(element)


###Second attempt

url_1 = 'https://www.cupones.es/'
page = requests.get(url_1)
soup = BeautifulSoup(page.content, 'html.parser')
descr = soup.find_all(class_='voucher-mainDetailsContentTitle')
#exp = soup.find_all(class_='voucherConditions-itemLabel')
my_elems = soup.find_all(class_='resultList-container resultList-container--primary')
for element in my_elems:
    for id_page in element.find_all(True,{'data-voucher':True}):
        str1 = id_page.get('data-voucher').split('"shop":')[1]
        str2 = str1.split(',')[0].replace('"', '')
        brands.append(str2)
for element in descr:
    description.append(element.text)   
#print(description)
#print(brands)
df = pd.DataFrame(columns = ['Deals', 'Shops']) 
df['Deals'] = description
df['Shops'] = brands
df.to_excel('Deals.xlsx', index=False, encoding='utf-8-sig')
sendEmail()



