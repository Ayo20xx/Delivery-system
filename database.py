import sqlite3

#make connection
connection=sqlite3.connect("sqlite")
#create cursor 
cursor=connection.cursor()
#1 create table 
cursor.execute("""
               CREATE TABLE IF NOT EXISTS shipment (
               id INTEGER PRIMARY KEY,
               content TEXT,
               weight REAL,
               status TEXT)""")

#2 add shipment data 
# cursor.execute("""INSERT INTO shipment
#                   VALUES(12702,'palm trees',8.5,'placed')
#                """)
#save data 
#3 read shipment 
# cursor.execute("""
#      SELECT status FROM shipment
#      WHERE content'
# """)


cursor.execute("""
UPDATE shipment SET status = 'in_transit'
WHERE id = 12701
""")

connection.commit()


# result= cursor.fetchall()
# print(result)
# connection.commit()
# #close when done 
# connection.close()