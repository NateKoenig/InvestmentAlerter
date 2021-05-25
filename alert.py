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
				body = "DOGE is up over 20% in the last 24 hours at {}%".format(price)
			elif price >= 10:
				body = "DOGE is up over 10% in the last 24 hours at {}%".format(price)
			elif price >= 5:
				body = "DOGE is up over 5% in the last 24 hours at {}%".format(price)
			else:
				body = "DOGE is up a bit in the last 24 hours at {}%".format(price)
		else:
			subject = "OUCH!"
			if price >= 20:
				body = "DOGE is down over 20% in the last 24 hours at {}%".format(price)
			elif price >= 10:
				body = "DOGE is down over 10% in the last 24 hours at {}%".format(price)
			elif price >= 5:
				body = "DOGE is down over 5% in the last 24 hours at {}%".format(price)
			else:
				body = "DOGE is down a bit in the last 24 hours at {}%".format(price)
	#otherwise if they're both positive, only message something if there's a new threshold
	elif curPriceUpOrDown == "up":
		subject = "LET'S GO!"
		if price >= 20 and lastPrice <20:
			body = "DOGE is up over 20% in the last 24 hours at {}%".format(price)
		elif price >= 10 and price < 20 and (lastPrice >=20 or lastPrice < 10):
			body = "DOGE is up over 10% in the last 24 hours at {}%".format(price)
		elif price >= 5 and price < 10 and (lastPrice >=10 or lastPrice < 5):
			body = "DOGE is up over 5% in the last 24 hours at {}%".format(price)
		else:
			messageSomething = 0 #do nothing, no significant change
	#otherwise, they're both negative, only message something if there's a new threshold
	else:
		subject = "OUCH!"
		if price >= 20 and lastPrice <20:
			body = "DOGE is down over 20% in the last 24 hours at {}%".format(price)
		elif price >= 10 and price < 20 and (lastPrice >= 20 or lastPrice < 10):
			body = "DOGE is down over 10% in the last 24 hours at {}%".format(price)
		elif price >= 5 and price < 10 and (lastPrice >= 10 or lastPrice < 5):
			body = "DOGE is down over 5% in the last 24 hours at {}%".format(price)
		else:
			messageSomething = 0 #do nothing, no significant change

	#make this an option later, for now send to me (verizon)
	to = "then number or email you want to send the message to"


	#calls message alert only if we need to message something
	if messageSomething == 1:
		messageAlert(subject, body, to)


# Creates message alert
def messageAlert(subject, body, to):
	#use EmailMessage library and set variables based on function arguments
	msg.set_content(body)
	msg['subject'] = subject
	msg['to'] = to

	server.send_message(msg)



#new email and login
msg = EmailMessage()
user = "your sent from email"
msg['from'] = user
password = "your sent from email app password"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(user, password)


# Driver
if __name__ == '__main__':
	#create variables
	price = "this is a price"
	lastPrice = "100000.00"
	savePrice = "save this"
	count = 0

	#run infinitely
	while count != 36:
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

		count = count + 1 #so this program will run for 3 hours

	server.quit() #quit the server, we're done now


