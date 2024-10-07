import mysql.connector

dataBase = mysql.connector.connect(
	host = 'localhost',
	user = 'root', 
	passwd = 'DjangoPassword123',

	)

# cursor object
cursorObject = dataBase.cursor()

# database
cursorObject.execute("CREATE DATABASE lisdcrm")

print("All Done!")