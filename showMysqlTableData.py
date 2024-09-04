# To get and show table data from mysql database

import mysql.connector

connection = mysql.connector.connect(user = 'nagalakshmi', password ='Nagalakshmi@123', host = '138.68.140.83', database = 'dbNagalakshmi')
cursor = connection.cursor()
table = "item"

cursor.execute(f"desc {table}")
fields = cursor.fetchall()
fieldNames = [item[0] for item in fields]

cursor.execute(f"SELECT * FROM {table}")
records = cursor.fetchall()

for record in records:
	print("-"*25)
	for index,fieldValue in enumerate(record):
		print(f"{fieldNames[index]}: {fieldValue}")

connection.close()