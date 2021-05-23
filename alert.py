import smtplib
from email.message import EmailMessage

#IF PROBLEMS, IMPORT THE ABOVE LIBRARIES

from urllib.request import urlopen as uReq
from bs4 import BeautifySoup as soup


#TODO: make sure that it sends every time the price changes from what it currently is (ie from over 20 to over 10 etc)

def scrape():
	my_url = 'https://www.coindesk.com/price/dogecoin'

	#opening up connection, grabbing page
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()

	#html parsing
	page_soup = soup(page_html, "html.parser")

	#grab price diff %
	price = string(page_soup.findAll("span", {"class":"percent-value-text"}))

	#look at price % and decide what message to display
	subject = "This is the subject"
	body = "This is my message"

	print(price)

	if (price[0] != '-') {
		price = int(price)
		subject = "Yeah!"
		if (price >= 20) {
			body = "DOGE is up over 20% today at {}%".format(price)
		}
		else if (price >= 10) {
			body = "DOGE is up over 10% today at {}%".format(price)
		}
		else if (price >= 5) {
			body = "DOGE is up over 5% today at {}%".format(price)
		}
		else {
			body = "DOGE is down a bit today at {}%".format(price)
		}
	}
	else {
		price = price[1:]
		subject = "Oops!"
		if (price >= 20) {
			body = "DOGE is down over 20% today at {}%".format(price)
		}
		else if (price >= 10) {
			body = "DOGE is down over 10% today at {}%".format(price)
		}
		else if (price >= 5) {
			body = "DOGE is down over 5% today at {}%".format(price)
		}
		else {
			body = "DOGE is down a bit today at {}%".format(price)
		}
	}

	#make this an option later, for now send to me (verizon)
	to = "your email or number"


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
	user = "your email"
	msg['from'] = user
	password = "your app key"


	#necessary to be able to send email/text, like a server from gmail
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(user, password)
	server.send_message(msg)

	server.quit() #quit the server, we're done now



scrape()

## Test function, send this stuff to my number (if you want email, just replace w/ email to send to)
#if __name___ == '__main__':
#	messageAlert("Hey", "Hello world", "put your phone number or email here")
