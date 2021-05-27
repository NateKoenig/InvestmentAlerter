import smtplib
from email.message import EmailMessage
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time

def webScrape():
	my_url = 'https://robinhood.com/crypto/ETH'

	#opening up connection and grab page
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()

	#html parsing
	page_soup = soup(page_html, "html.parser")

	#grab price diff %
	data = str(page_soup.findAll("span", {"class":"css-dq91k1"})[6].text)
	data = data[:-2]
	newData = ""
	for element in reversed(data):
		if element == '(':
			break
		else:
			newData += element
	newData = newData[::-1]
	return str(newData)


def createMessage(currentDelta, priorDelta):
	#initialize variables
	subject = "This is the subject"
	body = "This is my message"


	currentUpDown = "up"
	priorUpDown = "up"
	if priorDelta != currentDelta: #first check: string comparison to see if at least different, send message if not the same
		print("Not the same price")
		
		#the number or email that we're sending the message to. Make this an option later
		to = "your send to phone number or email"

		#second check pt1: get magnitudes of each
		if currentDelta[0] == '-':
			currentDelta = currentDelta[1:]
			currentUpDown = "down"
		currentDelta = float(currentDelta)

		if priorDelta[0] == '-':
			priorDelta = priorDelta[1:]
			priorUpDown = "down"
		priorDelta = float(priorDelta)

		#second check pt2: if the two are different in pos & neg and or the two are different by 1 percent or more, send message
		if currentUpDown != priorUpDown:
			print("One price was pos and one price was neg")
			#send message saying the price is now (up or down) by _____
			if currentDelta > 0:
				subject = "Good News!"
				body = "ETH is now up today at {}%".format(currentDelta)
				sendMessage(subject, body, to)
				print("Sent Message")
			else:
				subject = "Bad News!"
				body = "ETH is now down today at {}%".format(currentDelta)
				sendMessage(subject, body, to)
				print("Sent Message")
			return 'yes'
		elif abs(currentDelta - priorDelta) >= 1:
			print("Price differed by >= 1")
			if currentDelta > 0:
				#send message saying that the price is now up by ____
				subject = "Good News!"
				body = "ETH is still up today at {}%".format(currentDelta)
				sendMessage(subject, body, to)
				print("Sent Message")
			else:
				#send message saying that the price is now down by ____
				subject = "Bad News!"
				body = "ETH is still down today at {}%".format(currentDelta)
				sendMessage(subject, body, to)
				print("Sent Message")
			return 'yes'

	print("The current price is {}%".format(currentDelta))
	print("The last price messaged was {}%".format(priorDelta))
	return 'no'

def sendMessage(subject, body, to):
	#use EmailMessage library and set variables based on function arguments
	msg.set_content(body)
	msg['subject'] = subject
	msg['to'] = to

	server.send_message(msg)



if __name__ == '__main__':
	#email and login setup
	msg = EmailMessage()
	user = "your sent frome mail"
	msg['from'] = user
	password = "your sent from email app password"

	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(user, password)

	#set variables
	currentDelta = "this is the current percent change in price"
	priorDelta = "1000000"
	count = 0
	update = 'no'


	while count != 60: #this program will run for 1 hour
		#scrape the data
		currentDelta = webScrape()

		#creates and possibly sends message
		update = createMessage(currentDelta, priorDelta)

		#copy over the last currentDelta
		#priorDelta = currentDelta <-- Can't do this, or if increases or decreases little by little we'll never be alerted
		if (update == 'yes'):
			priorDelta = currentDelta

		print('----------This was cycle {}----------'.format(count))
		time.sleep(60) #wait 1 minute before checking again
		count = count + 1

	server.quit()


