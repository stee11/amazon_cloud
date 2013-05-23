#This is a program made by Steven Kolln
#This program demonstrates basic usage of the AWS service SES

import boto;

def main():
	ses=boto.connect_ses();
	print;
	print ses.get_send_statistics();
	print;
	
	raw_input("Going to verify my email and print the valid emails.");
	print;
	#ses.verify_email_address("your email1");
	#ses.verify_email_address("your email 2");
	#ses.verify_email_address("your email 3");
	for l in ses.list_verified_email_addresses().VerifiedEmailAddresses:
		print l;
	print;
	sendTo=raw_input("Enter the email you would like to send to from xxx@xxx.xxx: ");
	ses.send_email("xxx@xxx.xxx", "Hello from SES!", "Hello "+sendTo+", from Amazon SES!",sendTo);
	raw_input("Email should be sent to kollns1. Check email. Quota and statistics will now be printed.");
	print;
	#printing quotas
	print "Max sends per 24 hours: ",
	print ses.get_send_quota().GetSendQuotaResponse.GetSendQuotaResult.Max24HourSend;
	print "Mail sent per last 24 hours: ",
	print ses.get_send_quota().GetSendQuotaResponse.GetSendQuotaResult.SentLast24Hours;
	print "Max send rate is: ",
	print ses.get_send_quota().GetSendQuotaResponse.GetSendQuotaResult.MaxSendRate;
	#printing stat 215's
	print;
	for r in ses.get_send_statistics().SendDataPoints:
		print "Number of Complaints: ",
		print r.Complaints;
		print "Timestamp: ",
		print r.Timestamp;
		print "Number of Attempts: ",
		print r.DeliveryAttempts;
		print "Number of Bounces: ",
		print r.Bounces;
		print "Number of Rejects: ",
		print r.Rejects;
		
	print;
	raw_input("Wer're gong to send an email!");
	while True:
		cc=list();
		bcc=list();
		result=raw_input("Would you like to CC someone? Type yes or no: ").lower();
		if result[:1]=="y":
			while True:
				person=raw_input("Who would you like to add: ");
		if result[:1]=="y":
			while True:
				person=raw_input("Who would you like to add: ");
				bcc.append(person);
				if raw_input("Would you like to add another yes or no: ").lower()[:1]=="n":
					break;
		
		newEmail=raw_input("Add a new email to send an email from: ");
		ses.verify_email_address(newEmail);
		raw_input("Press enter once the email is received and accepted.");
		send_mail=raw_input("Would you like to send a message with these credentials? Yes or No: ");
		if send_mail.lower()[:1]=="y":
			to=raw_input("Enter who you would like to send to: ");
			ses.send_email(newEmail, "Hello from SES!", "Hello "+to+", from Amazon SES!",to, cc, bcc);
		print;
		print("Here are all the emails verified.");
		for l in ses.list_verified_email_addresses().VerifiedEmailAddresses:
			print l;
		toDelete=raw_input("Choose an email to delete from the list: ");
		try:
			ses.delete_verified_email_address(toDelete);
		except:
			print toDelete,
			print "Is not a valid email.";
		raw_input("Processing. . . . . . .");
		print("Here are all the emails verified after deletion.");
		for l in ses.list_verified_email_addresses().VerifiedEmailAddresses:
			print l;
		break;
			
		
		
	

if __name__ == "__main__":
	main();