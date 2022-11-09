import mysql.connector
"""
Connection to the server.
The username is root, the password is 1234 and the hostname is localhost
""" 
#db=mysql.connector.connect(user="python",passwd="123456",host="localhost",port="5000") 
 
db=mysql.connector.connect(user="python",passwd="123456",host="localhost",port="5000", database='Logger')
 
my_cursor=db.cursor()
query="SHOW DATABASES" #query to show all the tables in the database
my_cursor.execute(query)
for tab in my_cursor: #printing all the tables
    print(tab)