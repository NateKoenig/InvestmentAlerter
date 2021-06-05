import smtplib
from email.message import EmailMessage
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time




# Scrapes Robinhood for price (just ETH for now)
def webScrape():
	my_url = 'https://finance.yahoo.com/quote/BTC-USD?p=BTC-USD&.tsrc=fin-srch'

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
	print('sent message')

	del msg['to']





# Driver
if __name__ == '__main__':
	#email and login setup
	msg = EmailMessage()
	user = "your sent from email"
	msg['from'] = user
	password = "your send from email app password"

	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(user, password)


	#intialize variables
	currentChange = 1.0
	priorChange = 1000.0
	subject = 'This is a subject'
	body = 'This is a body'
	to = "put your send to phone number or email here" #the number or email that we're sending the message to. Make this an option later
	count = 0



	#get initial % change in price 
	priorChange = webScrape()
	#TODO: (send message stating that this is what we'll go off of)
	subject = 'INITIAL'
	body = 'This is the first message. Sending alerts when a % change in daily price differs by 1 or more, starting at {}%'.format(priorChange)
	sendMessage(body, subject, to)



	#enter while loop that will continue to run program
	while count != 60:
		print('------This is loop {}------'.format(count + 1))
		print('Previous change: {}'.format(priorChange))

		#get current 24 hour % change
		currentChange = webScrape()
		print('Current change: {}'.format(currentChange))

		if currentChange != priorChange:
			if priorChange > 0 and currentChange < 0:
				#output message saying it's now down today
				subject = 'DOWN'
				body = 'ETH is now down today at {}%'.format(currentChange)
				sendMessage(body, subject, to)

				#set prior to now be current
				priorChange = currentChange
			elif priorChange < 0 and currentChange > 0:
				#output message saying it's now up today
				subject = 'UP'
				body = 'ETH is now up today at {}%'.format(currentChange)
				sendMessage(body, subject, to)

				#set prior to now be current
				priorChange = currentChange
			elif currentChange > 0:
				if currentChange - priorChange >= 1:
					#output message saying that it's now up even more today at ___
					subject = 'UP'
					body = 'ETH is now up even more today at {}%'.format(currentChange)
					sendMessage(body, subject, to)

					#set prior to now be current
					priorChange = currentChange
				elif currentChange - priorChange <= -1:
					#output message saying that it's now up less today at ___
					subject = 'UP'
					body = 'ETH is now up less today at {}%'.format(currentChange)
					sendMessage(body, subject, to)

					#set prior to now be current
					priorChange = currentChange
			elif currentChange < 0:
				if currentChange - priorChange >= 1:
					#ouptut message saying that it's now down even more today at ___
					subject = 'DOWN'
					body = 'ETH is now down even more today at {}%'.format(currentChange)
					sendMessage(body, subject, to)

					#set prior to now be current
					priorChange = currentChange
				elif currentChange - priorChange <= -1:
					#output message saying that it's now down less today at ___
					subject = 'DOWN'
					body = 'ETH is now down less today at {}%'.format(currentChange)
					sendMessage(body, subject, to)

					#set prior to now be current
					priorChange = currentChange

		#wait 2 minutes before entering loop again, making this program go on for 2 hours w/ how the while loop is set up
		time.sleep(120)

		count = count + 1

	#exits while loop, we are done			
	server.quit()

			
