#This is a program made by Steven Kolln
#This program demonstrates basic usage of the AWS service S3

#Imports classes from Library
from boto import *; 
from boto.s3.lifecycle import Lifecycle; 
from boto.s3.key import Key;


def main():
	raw_input("I am about to create a bucket called 'test_bucket1' and a\n text file called 'HelloWorld.txt'. Press enter to continue.");
	print;
	with open("HelloWorld.txt", "w") as f:
		f.writelines("I hope you can read this file!");
	s3=boto.connect_s3();
	bucket1=s3.create_bucket('test_bucket1'); #creates an s3 bucket.
	print "'test_bucket1' should be created. GO CHECK! Press enter to continue.";
	raw_input();
	#I am going to create two new keys
	raw_input("I am going to add a textfile and picture to S3. Press enter to continue.");
	k=Key(bucket1);
	picture=Key(bucket1);
	picture.key="picture";
	picture.set_contents_from_filename("bearandi.jpg");
	k.key="helloWorld";
	k.set_contents_from_filename("helloWorld.txt");
	print;
	raw_input("Look at the files on S3. The Files will now be downloaded. Enter to continue.");
	print;
	#This line and the next download the files from S3
	picture.get_contents_to_filename("newBear.jpg"); 
	k.get_contents_to_filename("newHelloWorld.txt");
	#delete a key
	raw_input("File downloads 100% I am now going to delete the text file. Enter to continue.");
	print;
	#delete the text file.
	bucket1.delete_key("helloWorld");
	raw_input("The text file should now be deleted. I am now going to create 3 more buckets \nand delete one. Press enter to continue.");
	print;
	#create more buckets
	bucket2=s3.create_bucket("lab1_bucket2");
	bucket3=s3.create_bucket("lab1_bucket3");
	bucket4=s3.create_bucket("lab1_bucket4");
	raw_input("The buckets were created. I will now delete lab1_bucket4.");
	print;
	bucket4.delete();
	raw_input("lab1_bucket4 deleted. I will now querry to see if buckets exist and if I have permision.");
	print;
	#find buckets
	print "I am going to try the bucket names 'test_bucket1', which exists, and 'lab1_bucket4', which does not."
	print;
	print "Here is a list of all buckets:";
	print s3.get_all_buckets();
	print;
	try:
		print "test_bucket1:",
		print bucket1.get_acl();
	except NameError:
		print "The bucket 'bucket1' name does not exist.";
	try:
		print "lab1_bucket4:",
		print bucket4.get_acl();
	except :
		print "That bucket 'lab1_bucket4' does not exist. Invalid name.";
	print;
	raw_input("I am now going to copy the picture from test_bucket1 to lab1_bucket2.");
	#move object
	print;
	#kill object in 5 days
	picture.copy("lab1_bucket2","Bucket2Bear.jpg");
	raw_input("There should now be a copied picture in lab1_bucket2.\nI will now add a new photo with a 5 day expiration and with reduced redundancy in bucket 3.");
	print;
	cycle=Lifecycle();
	k3=Key(bucket3);
	cycle.add_rule("Five Days", "My Second picture", "Enabled", 5);
	bucket3.configure_lifecycle(cycle);
	k3.key="My Second picture";
	k3.set_contents_from_filename("GW2.jpg", reduced_redundancy=True);
	raw_input("Check bucket3 for the new object with redundancy and an expiration.\nThe last bucket with versioning is going to be made.");
	print;
	#create last bucket
	lastBucket=s3.create_bucket("last_bucket");
	lastBucket.configure_versioning(True, False, None);
	print "Version Status: ", #print versioning status
	print lastBucket.get_versioning_status();
	print;
	lastK=Key(lastBucket);
	lastK.name="MyFile";
	lastK.set_contents_from_filename("helloWorld.txt"); #add original hello world
	print "Added a hello world containing the string: '",
	print lastK.get_contents_as_string();
	print;
	#editted the same hello world
	with open("helloWorld.txt", "a") as f:
		f.writelines("\nI added some lines.\nLast Line.");
	lastK.name="MyFile";
	lastK.set_contents_from_filename("helloWorld.txt");
	print "Added a hello world containing the string: '",
	print lastK.get_contents_as_string();
	print;
	print "'.\nObject details: ";
	for version in lastBucket.list_versions():
		print version.name;
		print version.version_id;
		print;
		print;
	toDelete=raw_input("There should now be two different versions. Type the version of the file you would like to delete: ");
	try:
		print lastBucket.delete_key("MyFile", version_id=toDelete);
	except:
		print;
	raw_input("Version of the file you entered should be deleted.");
	lastK.set_metadata("My meta data", "This is the meta data");
	print; lastK.get_metadata("My meta data");
	
	
	
	
	

	





if __name__ == "__main__":
	main();