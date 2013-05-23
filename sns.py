#This is a program made by Steven Kolln
#This program demonstrates basic usage of the AWS service SNS

import boto;
import boto.ec2.cloudwatch
def showTopics(dic):
	for length in range(0, len(dic)):
		for x, y in dic[length].items():
			print x, y
def printinfo(arn):
	sns=boto.connect_sns();
	dic= sns.get_topic_attributes(arn)['GetTopicAttributesResponse']['GetTopicAttributesResult']['Attributes']
	for x, y in dic.items():
		if x=="EffectiveDeliveryPolicy" or x=="Policy":
			pass
		else:
			print x, y
			print ""
	print dic['EffectiveDeliveryPolicy']
	print ""
	print dic['Policy']
	print ""

def main():
	sns=boto.connect_sns();
	raw_input("Going to create the alpha and beta topics. Enter to continue");
	sns.create_topic("Alpha1");
	sns.create_topic("Beta1");
	raw_input("Alpha and Beta topics made. Here is the list of topics.");
	dic=sns.get_all_topics()['ListTopicsResponse']['ListTopicsResult']['Topics'];
	print dic;
	showTopics(dic);
	delete=raw_input("I am now going to delete the Beta topic. Copy beta and enter it here: ");
	sns.delete_topic(delete);
	arn=raw_input("Beta was deleted here is the new list of topics.");
	dic=sns.get_all_topics()['ListTopicsResponse']['ListTopicsResult']['Topics'];
	showTopics(dic);
	arn=raw_input("We are now going to subscribe to the alpha topic. Copy and paste alpha here: ");
	sns.subscribe(arn, "email", "xxx@xxx.xxx");
	print arn;
	sns.subscribe(arn, "email-json", "xxx@xxx.xxx");
	sns.subscribe(arn, "http", "http://cloud.comtor.org/csc470logger/logger");
	raw_input("There should now be 3 subscriptions added to the topic. Go check in console if needed. \nHere are the detials");
	printinfo(arn)
	raw_input("I am now going to change the display name for the topic.");
	sns.set_topic_attributes(arn,"DisplayName", "NewName");
	raw_input("Name change made. The new information is... ");
	printinfo(arn)
	raw_input("I am now going to send a message to all of those who have subscribed.");
	print sns.publish(arn, "Hello classmates. What is int?");
	raw_input("Message sent. Please check mail.");
	raw_input("We are now going to make a cloud watch alarm.");
	cw=boto.connect_cloudwatch()
	myMetric=cw.list_metrics()[0]
	print cw.describe_alarms()[0]
	cw.create_alarm(cw.describe_alarms()[0])
	
	
if __name__ == "__main__":
	main();
	