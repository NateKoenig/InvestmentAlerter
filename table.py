from flask import Flask, render_template, request
import smtplib
from email.message import EmailMessage
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time

app = Flask(__name__)

# Scrapes Robinhood for price (just ETH for now)
def webScrape(ticker):
	if ticker == 'BTC' or ticker == 'ETH' or ticker == 'DOGE':
		if ticker == 'BTC':
			my_url = 'https://finance.yahoo.com/quote/BTC-USD?p=BTC-USD&.tsrc=fin-srch'
		elif ticker == 'ETH':
			my_url = 'https://finance.yahoo.com/quote/ETH-USD?p=ETH-USD&.tsrc=fin-srch'
		elif ticker == 'DOGE':
			my_url = 'https://finance.yahoo.com/quote/DOGE-USD?p=DOGE-USD&.tsrc=fin-srch'

		#opening up connection and grab page
		uClient = uReq(my_url)
		page_html = uClient.read()
		uClient.close()

		#html parsing
		page_soup = soup(page_html, "html.parser")

		#grab price diff %
		data = str(page_soup.findAll("span", {"data-reactid":"34"})[1].text)

		data = data[:-2]
		newData = ""
		for element in reversed(data):
			if element == '(':
				break
			else:
				newData += element
		newData = newData[::-1]
		return float(newData)




# Handles sending the sms mesage
def sendMessage(body, subject, to):
	#use EmailMessage library and set variables based on function arguments
	msg.set_content(body)
	msg['subject'] = subject
	msg['to'] = to

	server.send_message(msg)

	del msg['to']
	del msg['subject']


# Drives the program
def driver(ticker, number, carrier):
	#email and login setup
	user = "sent from email"
	msg['from'] = user
	password = "sent from email app password"
	carrierEmail = "some email string"
	
	if carrier == "VERIZON" or carrier == "XFINITY":
		carrierEmail = "vtext.com"
	elif carrier == "AT&T":
		carrierEmail = "txt.att.net"
	elif carrier == "SPRINT":
		carrierEmail = "messaging.sprintpcs.com"
	elif carrier == "TMOBILE":
		carrierEmail = "tmomail.net"
	elif carrier == "VIRGIN":
		carrierEmail = "vmobl.com"

	to = number + "@" + carrierEmail

	#server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(user, password)

	count = 0



	#get initial % change in price 
	priorChange = webScrape(ticker)
	#TODO: (send message stating that this is what we'll go off of)
	subject = 'INITIAL'
	body = 'Welcome to Cereal! You will get alerts for {} when a change in daily price differs by 1%, starting at {}%.'.format(ticker, priorChange)
	sendMessage(body, subject, to)



	#enter while loop that will continue to run program
	while count != 60:
		#print('------This is loop {}------'.format(count + 1))
		#print('Previous change: {}'.format(priorChange))

		#get current 24 hour % change
		currentChange = webScrape(ticker)
		#print('Current change: {}'.format(currentChange))

		if currentChange != priorChange:
			if priorChange > 0 and currentChange < 0:
				#output message saying it's now down today
				subject = 'DOWN'
				body = '{} is now down today at {}%'.format(ticker, currentChange)
				sendMessage(body, subject, to)

				#set prior to now be current
				priorChange = currentChange
			elif priorChange < 0 and currentChange > 0:
				#output message saying it's now up today
				subject = 'UP'
				body = '{} is now up today at {}%'.format(ticker, currentChange)
				sendMessage(body, subject, to)

				#set prior to now be current
				priorChange = currentChange
			elif currentChange > 0:
				if currentChange - priorChange >= 1:
					#output message saying that it's now up even more today at ___
					subject = 'UP'
					body = '{} is now up even more today at {}%'.format(ticker, currentChange)
					sendMessage(body, subject, to)

					#set prior to now be current
					priorChange = currentChange
				elif currentChange - priorChange <= -1:
					#output message saying that it's now up less today at ___
					subject = 'UP'
					body = '{} is now up less today at {}%'.format(ticker, currentChange)
					sendMessage(body, subject, to)

					#set prior to now be current
					priorChange = currentChange
			elif currentChange < 0:
				if currentChange - priorChange >= 1:
					#ouptut message saying that it's now down even more today at ___
					subject = 'DOWN'
					body = '{} is now down less today at {}%'.format(ticker, currentChange)
					sendMessage(body, subject, to)

					#set prior to now be current
					priorChange = currentChange
				elif currentChange - priorChange <= -1:
					#output message saying that it's now down less today at ___
					subject = 'DOWN'
					body = '{} is now down even more today at {}%'.format(ticker, currentChange)
					sendMessage(body, subject, to)

					#set prior to now be current
					priorChange = currentChange

		#wait 2 minutes before entering loop again, making this program go on for 2 hours w/ how the while loop is set up
		time.sleep(120)

		count = count + 1

	#exits while loop, we are done			
	server.quit()


# Displays homepage
@app.route("/", methods =["GET", "POST"])
def home():
	if request.method == "POST":
		#get info from html form
		ticker = request.form.get("ticker")
		number = request.form.get("number")

		#drives the program
		driver(ticker, number, carrier)

		return "done"

	return render_template("home.html")

# Starts the program
if __name__ == '__main__':
	#initialize variables
	msg = EmailMessage()
	server = smtplib.SMTP("smtp.gmail.com", 587)
	currentChange = 1.0
	priorChange = 1000.0
	subject = 'This is a subject'
	body = 'This is a body'
	to = "dummy number" #the number or email that we're sending the message to. Make this an option later

	app.run()



