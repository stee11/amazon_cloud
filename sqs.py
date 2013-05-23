#This is a program made by Steven Kolln
#This program demonstrates basic usage of the AWS service SNS

import boto;


def queueInfo():
	sqs=boto.connect_sqs();
	queue1=raw_input("Input the name of a queue here and press enter: ");
	print ""
	raw_input("Here is some info about the queue:");
	q1=sqs.get_queue_attributes(sqs.get_queue(queue1));
	for x,y in q1.items():
		print x,y
		print ""

def main():
	sqs=boto.connect_sqs();
	raw_input("I am now going to create two queues.");
	sqs.create_queue("test");
	sqs.create_queue("test2");
	raw_input("Two queues were made. I am now going to list all queues I own.");
	for x in sqs.get_all_queues():
		print x
	queueInfo();
	queueInfo();
	raw_input("I am now going to delete queue 2. \n");
	sqs.delete_queue(sqs.get_queue("test2"));
	raw_input("Queue deleted. Here are the queues that are left.");
	print sqs.lookup("test");
	print sqs.lookup("test2");
	raw_input("I am now going to add 3 message to the queue. Test1 2 and 3.");
	for x in range(1,4):
		sqs.get_queue("test").write(sqs.get_queue("test").new_message("This is a Test"+str(x)));
	q1=sqs.get_queue_attributes(sqs.get_queue("test"));
	for x,y in q1.items():
		if x=="ApproximateNumberOfMessages":
			print x,y
			print ""
	raw_input("I am now going to dequeue the queue one by one then delete the queue");
	print str(sqs.get_queue("test").read().get_body())
	raw_input("First message dequeued. Here are the next two.");
	print sqs.get_queue("test").read().get_body()
	print sqs.get_queue("test").read().get_body()
	raw_input("Queue empty. Now deleting the queue");
	sqs.delete_queue(sqs.get_queue("test"));
	print sqs.lookup("test");
	print sqs.lookup("test2");
	





if __name__=="__main__":
	main();