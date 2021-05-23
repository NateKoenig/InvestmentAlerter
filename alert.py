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
	return str(page_soup.findAll("span", {"class":"percent-value-text"})[0].text)

def createMessage(price, lastPrice, curPriceUpOrDown, lasPriceUpOrDown):
	#initialize variables
	subject = "This is the subject"
	body = "This is my message"
	messageSomething = 1

	#if the current and last price differ over the 0% price line, then we update
	if curPriceUpOrDown != lasPriceUpOrDown:
		if curPriceUpOrDown == "up":
			subject = "LET'S GO!"
			if price >= 20:
				body = "DOGE is up over 20% today at {}%".format(price)
			elif price >= 10:
				body = "DOGE is up over 10% today at {}%".format(price)
			elif price >= 5:
				body = "DOGE is up over 5% today at {}%".format(price)
			else:
				body = "DOGE is up a bit today at {}%".format(price)
		else:
			subject = "OUCH!"
			if price >= 20:
				body = "DOGE is down over 20% today at {}%".format(price)
			elif price >= 10:
				body = "DOGE is down over 10% today at {}%".format(price)
			elif price >= 5:
				body = "DOGE is down over 5% today at {}%".format(price)
			else:
				body = "DOGE is down a bit today at {}%".format(price)
	#otherwise if they're both positive, only message something if there's a new threshold
	elif curPriceUpOrDown == "up":
		if price >= 20 and lasPrice <20:
			body = "DOGE is up over 20% today at {}%".format(price)
		elif price >= 10 and (lasPrice >=20 or lasPrice < 10):
			body = "DOGE is up over 10% today at {}%".format(price)
		elif price >= 5 and (lasPrice >=10 or lasPrice < 5):
			body = "DOGE is up over 5% today at {}%".format(price)
		else:
			messageSomething = 0 #do nothing, no significant change
	#otherwise, they're both negative, only message something if there's a new threshold
	else:
		if price >= 20 and lasPrice <20:
			body = "DOGE is down over 20% today at {}%".format(price)
		elif price >= 10 and (lasPrice >= 20 or lasPrice < 10):
			body = "DOGE is down over 10% today at {}%".format(price)
		elif price >= 5 and (lasPrice >= 10 or lasPrice < 5):
			body = "DOGE is down over 5% today at {}%".format(price)
		else:
			messageSomething = 0 #do nothing, no significant change

	#make this an option later, for now send to me (verizon)
	to = "the number/email you want to send to goes here"


	#calls message alert only if we need to message something
	if messageSomething == 1:
		messageAlert(subject, body, to)


# Creates message alert
def messageAlert(subject, body, to):
	#use EmailMessage library and set variables based on function arguments
	msg = EmailMessage()
	msg.set_content(body)
	msg['subject'] = subject
	msg['to'] = to

	#new email
	user = "your sent from email goes here"
	msg['from'] = user
	password = "your sent from email app password goes here"


	#necessary to be able to send email/text, like a server from gmail
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(user, password)
	server.send_message(msg)

	server.quit() #quit the server, we're done now



# Driver
if __name__ == '__main__':

	thing = "10.0"
	thing2 = float(thing)

	#create variables
	price = "this is a price"
	lastPrice = "100000.00"

	#run infinitely
	while True:
		price = scrape()
		savePrice = price

		if price[0] != '-':
			if lastPrice[0] != '-':
				createMessage(float(price), float(lastPrice), "up", "up")
			else:
				lastPrice = float(lastPrice[1:])
				createMessage(float(price), lastPrice, "up", "down")
		else:
			price = float(price[1:])
			if lastPrice[0] != '-':
				createMessage(price, float(lastPrice), "down", "up")
			else:
				lastPrice = float(lastPrice[1:])
				createMessage(float(price), lastPrice, "down", "down")

		lastPrice = savePrice #update last price

		time.sleep(300) #wait 300s (5 min) before re-entering the cycle
