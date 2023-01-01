import requests
from bs4 import BeautifulSoup
import sys
import smtplib
import time

# provide link to desired item below
#URL = input("Enter the Amazon link: ")
#email = input("Enter the email you want to be alerted at: ")

email = sys.argv[1]
URL = sys.argv[2]


# You just need add to your header referer exactly the same as URL. headers = {"User-Agent" : "Your User Agent", "Regerer" : URL}
headers = {"User-Agent" : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15', "Regerer" : URL}
	


def check_price():
	page = requests.get(URL, headers=headers)

	soup = BeautifulSoup(page.content, 'html.parser')

	title = soup.find(id="productTitle").get_text()

	price = soup.find(id="corePriceDisplay_desktop_feature_div").get_text()
	price1=(price.split('$'))
	price2=(price1[1])
	price3 = price2.replace(',','')
	
	current_price = float(price3)

	try:
		high_price = (price1[3])
		high_price2 = high_price.replace(',','')
		converted_high = float(high_price2)	
		if(current_price < converted_high):
			send_mail()
	except IndexError:
		print("This item does not appear to be on sale")
	

def send_mail():
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	
	server.login(email,'iafxsfdvdaxfnpij')
	
	subject = 'Price drop on your item'
	body = ('Check the amazon link: ',URL)
	
	msg = f"Subject: {subject}\n\n{body}"
	
	server.sendmail(
			email,
			email,
			msg
			)
	print("Email has been sent")
			
	server.quit()

check_price()	
