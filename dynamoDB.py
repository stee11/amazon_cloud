#This is a program made by Steven Kolln
#This program demonstrates basic usage of the AWS service DynamoDB

import boto
import urllib2
import boto.dynamodb.condition as condition

def createTable(nam, schem):
	db=boto.connect_dynamodb();
	table=db.create_table(
		name=nam,
		schema=schem,
		read_units=1,
		write_units=1
		)
	return table

def main():
	db=boto.connect_dynamodb();
	raw_input("I am now going to create two tables called zipcodes and zipcodes2. Press enter to continue.");
	schema1=db.create_schema(
		hash_key_name='zip codes',
		hash_key_proto_value=str
		)
	schema2=db.create_schema(
		hash_key_name='town',
		hash_key_proto_value=str,
		range_key_name='person',
		range_key_proto_value=str
		)
	try:
		table1=createTable('zipcodes',schema1);
	except:
		pass
	try:
		table2=createTable('zipcodes2',schema2);
	except:
		pass
	for x in db.list_tables():
		print db.get_table(x)
	table1=db.get_table('zipcodes');
	table2=db.get_table('zipcodes2');
	raw_input("Here is a description of each table in my account. First table 1 then table 2.");
	for x in db.list_tables():
		print ""
		for a,b in db.describe_table(x)['Table'].items():
			print a,b
	raw_input("I am now going to add the data from the text file online.\n");
	text=urllib2.urlopen("https://s3.amazonaws.com/depasquale/datasets/zipcodes.txt")
	for x in range (0,20):
		 y=text.readline().split(',');
		 zip=y[0].replace('"','');
		 #print zip;
		 long=float(y[1].replace('"',''));
		 lat=float(y[2].replace('"',''));
		 town=y[3].replace('"','');
		 city=y[4].replace('"','');
		 lName=y[5].replace('"','');
		 fName=y[6].replace('"','');
		 item_data={
			'long': long,
			'lat': lat,
			'town': town,
			'city': city,
			'lName': lName,
			'fName': fName,
		}
		 item=table1.new_item(
			hash_key=zip,
			attrs=item_data
		)
		 #print item
		 item.put();
		#for z in range(0,len(y)):
		#	if (z!=2 or z!=1):
		#		print y[z].replace('"','')
		#	else:
		#		print y[z]
	raw_input("First table loaded. Time to load the second!");
	#Seconds table
	text2=urllib2.urlopen("https://s3.amazonaws.com/depasquale/datasets/zipcodes.txt")
	for x in range (0,40):
		 y=text2.readline().split(',');
		 zip=y[0].replace('"','');
		 long=float(y[1].replace('"',''));
		 lat=float(y[2].replace('"',''));
		 town=y[3].replace('"','');
		 city=y[4].replace('"','');
		 lName=y[5].replace('"','');
		 fName=y[6].replace('"','');
		 item_data={
			'long': long,
			'lat': lat,
			'town': town,
			'lName': lName,
			'fName': fName,
		}
		 item=table2.new_item(
			hash_key=town,
			range_key=zip,
			attrs=item_data
		)
		 item.put();
		#for z in range(0,len(y)):
		#	if (z!=2 or z!=1):
		#		print y[z].replace('"','')
		#	else:
		#		print y[z]
	raw_input("Done loading the second table...\n");
	raw_input("Here are the results for Table 1 Hash Key only table zips > 00610:")
	print ""
	result=table1.scan(
		scan_filter={'zip codes': condition.GT("00610")}
	)
	for x in result:
		print x
	print ""
	raw_input("Table 2 query: City name is ARECIBO:");
	print ""
	result=table2.query(
		hash_key="ARECIBO"
	)
	for x in result:
		print x;
	print ""
	raw_input("Table 2 query: City name greater than ARECIBO:")
	print ""
	result=table2.scan(
		scan_filter={'town': condition.GT("ARECIBO")}
	)
	for x in result:
		print x
	print ""
	zipToDelete=raw_input("Let's delete a record. Enter a record with a zip to delete from table1: ");
	toDelete=table1.scan(
		scan_filter={'zip codes': condition.EQ(zipToDelete)}
	)
	for x in toDelete:
		print x
	raw_input("The tupple above is going to be removed after enter");
	expected_value={'zip codes': zipToDelete}
	table1.get_item(zipToDelete).delete()
	raw_input("The Vale should be deleted. Go check!");
	zipToDelete=raw_input("Let's change a record. Enter the zip of the record to change: ");
	field=raw_input("enter the name of the field to change: ")
	changeTo=raw_input("What would you like to change it too?: ");
	ourItem=table1.get_item(
		hash_key=zipToDelete
	)
	ourItem[field]=changeTo;
	ourItem.put();
	raw_input("Value changed. I am going to change the throughput for both of the tables.");
	#try:
	#	table1.update_throughput(2,2);
	#except:
	#	print "error"
	raw_input("Table1 throughput changed");
	try:
		table2.update_throughput(3,3);
	except:
		print "error"
	raw_input("Table2 throughput changed");
	raw_input("I am now going to delete both tables. Press enter to delete.");
	try:
		table1.delete();
		table2.delete();
	except:
		pass
	
	
if __name__=="__main__":
	main();

