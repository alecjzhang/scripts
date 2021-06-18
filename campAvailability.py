import requests
from datetime import datetime
import smtplib, ssl
import time

url = 'https://www.recreation.gov/api/permits/72192/availability/nextavailable'
header = {
  	'authority': 'www.recreation.gov',
	'cache-control': 'max-age=0',
  	'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
  	'sec-ch-ua-mobile': '?0',
  	'upgrade-insecure-requests': '1',
  	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36',
  	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  	'sec-fetch-site': 'none',
  	'sec-fetch-mode': 'navigate',
  	'sec-fetch-user': '?1',
  	'sec-fetch-dest': 'document',
  'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}
end = datetime.strptime('2021-08-01','%Y-%m-%d')
start = datetime.strptime('2021-07-01','%Y-%m-%d')

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "alecjzhang@gmail.com"
receiver_email = "alecjzhang@gmail.com"
# get your gmail pass code from: https://myaccount.google.com/security, click on 'App passwords'
password = "sample code"


def query():
	r = requests.get(url, headers = header)
	date_str = r.json()['payload']
	print(date_str)
	return date_str

def email(date_str):
	message = 'Subject: Lost Cost: ' + date_str
	context = ssl.create_default_context()
	with smtplib.SMTP(smtp_server, port) as server:
	    server.ehlo()  # Can be omitted
	    server.starttls(context=context)
	    server.ehlo()  # Can be omitted
	    server.login(sender_email, password)
	    server.sendmail(sender_email, receiver_email, message)

while(True):
	date_str = query()
	date = datetime.strptime(date_str,'%Y-%m-%dT00:00:00Z')
	if date < end and date > start:
		print('WOW! Emailed\n')
		email(date_str)
		exit;
	else:
		time.sleep(60)
