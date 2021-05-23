import smtplib
from email.message import EmailMessage

#IF PROBLEMS, IMPORT THE ABOVE LIBRARIES

# Creates email alert
def email_alert(subject, body, to):
	#use EmailMessage library and set variables based on function arguments
	msg = EmailMessage()
	msg.set_content(body)
	msg['subject'] = subject
	msg['to'] = to

	#new email
	user = "this is your email needed"
	msg['from'] = user
	password = "this is your app password"


	#necessary to be able to send email, like a server from gmail
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(user, password)
	server.send_message(msg)

	server.quit() #quit the server, we're done now

# Test function, send this stuff to my number (if you want email, just replace w/ email to send to)
if __name___ == '__main__':
	email_alert("Hey", "Hello world", "put your phone number or email here")
