import smtplib
from email.message import EmailMessage
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time

def scrape():
	my_url = 'https://www.coindesk.com/price/dogecoin'

	#opening up connection, grabbing page
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()

	#html parsing
	page_soup = soup(page_html, "html.parser")

	#grab price diff %
	price = str(page_soup.findAll("span", {"class":"percent-value-text"})[0].text)

	#look at price % and decide what message to display
	subject = "This is the subject"
	body = "This is my message"

	if price[0] != '-':
		price = float(price)
		subject = "Yeah!"
		if price >= 20:
			body = "DOGE is up over 20% today at {}%".format(price)
		elif price >= 10:
			body = "DOGE is up over 10% today at {}%".format(price)
		elif price >= 5:
			body = "DOGE is up over 5% today at {}%".format(price)
		else:
			body = "DOGE is down a bit today at {}%".format(price)
	else:
		price = float(price[1:])
		subject = "Oops!"
		if price >= 20:
			body = "DOGE is down over 20% today at {}%".format(price)
		elif price >= 10:
			body = "DOGE is down over 10% today at {}%".format(price)
		elif price >= 5:
			body = "DOGE is down over 5% today at {}%".format(price)
		else:
			body = "DOGE is down a bit today at {}%".format(price)

	#make this an option later, for now send to me (verizon)
	to = "enter number or email"


	#calls message alert
	messageAlert(subject, body, to)


# Creates message alert
def messageAlert(subject, body, to):
	#use EmailMessage library and set variables based on function arguments
	msg = EmailMessage()
	msg.set_content(body)
	msg['subject'] = subject
	msg['to'] = to

	#new email
	user = "enter 'from' email"
	msg['from'] = user
	password = "enter your app key from that email"


	#necessary to be able to send email/text, like a server from gmail
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(user, password)
	server.send_message(msg)

	server.quit() #quit the server, we're done now



# Driver
if __name__ == '__main__':
	while True: #Infinite loop (create count variable later if want to only run for a certain period of time)
		scrape() #Execute the function, feeding it the last percentage
		time.sleep(600) #Wait 60s (10 min) before re-entering the cycle


