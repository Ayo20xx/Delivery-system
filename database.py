import sqlite3

#make connection
connection=sqlite3.connect("sqlite")
#create cursor 
cursor=connection.cursor()
#1 create table 
cursor.execute("""
               CREATE TABLE IF NOT EXISTS shipment (
               id INTEGER,
               content TEXT,
               weight REAL,
               status TEXT)""")

#2 add shipment data 
cursor.execute("""INSERT INTO shipment
                  VALUES(12701,'palm trees',8.5,'placed')
               """)
#save data 
connection.commit()
#close when done 
connection.close()