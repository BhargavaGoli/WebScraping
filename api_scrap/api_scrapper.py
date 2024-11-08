import requests
import xlwt
from xlwt import Workbook
import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.utils import COMMASPACE,formatdate


#globals
BASEURL='https://remoteok.com/api/'
USER_AGENT='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'

REQUEST_HEADERS={
    'User-Agent':USER_AGENT,
    'Accept-Language':"en-US, en;q=0.5"
}

def get_posting():
    res=requests.get(url=BASEURL,headers=REQUEST_HEADERS)
    return res.json()

def output_to_excel(data):
    wb=Workbook()
    job_sheet=wb.add_sheet('Jobs')

    headers=list(data[0].keys())

    for i in range(0,len(headers)):
        job_sheet.write(0,i,headers[i])
    
    for i in range(0,len(data)):
        job=data[i]
        values=list(job.values())
        for x in range(0,len(values)):
            job_sheet.write(i+1,x,values[x])
    wb.save('remote.xls')

#send email using smtp
def send_email(send_from,send_to,subject,text,files=None):
    assert isinstance(send_to,list)
    msg=MIMEMultipart()
    msg['From']=send_from
    msg['To']=COMMASPACE.join(send_to)
    msg['Date']=formatdate(localtime=True)
    msg['Subject']=subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f,'rb') as fil:
            part= MIMEApplication(fil.read(),Name=basename(f))
        part['Content-Dispostion']=f'attachment; filename="{basename(f)}"'
        msg.attach(part)

    smtp=smtplib.SMTP('smtp.gmail.com: 587')
    smtp.starttls()
    smtp.login(send_from,'lwhn bevj fgph hveh')
    smtp.sendmail(send_from,send_to,msg.as_string())
    smtp.close()


if __name__ == "__main__":
    j=get_posting()[1:]
    output_to_excel(j)
    send_email('gmssb7771@gmail.com',['zippo167891@gmail.com'],'job_postings','please find the attached text',files=['remote.xls'])
