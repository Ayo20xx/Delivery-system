# import sqlite3
# from .schemas import ShipmentCreate,ShipmentUpdate
# from typing import Any



# class Database:
#     def __init__(self):
#         self.conn=sqlite3.connect("sqlite.db",check_same_thread=False)
#         #create cursor 
#         self.cur=self.conn.cursor()
#         self.Create_table()
    
#     def Create_table(self):
#         self.cur.execute("""
#                     CREATE TABLE IF NOT EXISTS shipment (
#                     id INTEGER PRIMARY KEY,
#                     content TEXT,
#                     weight REAL,
#                     status TEXT,
#                     destination INTEGER)""")


#     def create(self,shipment:ShipmentCreate):
#         self.cur.execute("SELECT MAX (id) FROM shipment")
#         result = self.cur.fetchone()
#         new_id = (result[0] or 0) + 1
#         self.cur.execute("""INSERT INTO shipment
#                         VALUES(:id,:content,:weight,:status,:destination)
#                     """,
#                         {

#                         "id": new_id,
#                         **shipment.model_dump(),
#                         "status": "placed",

#                         }
#                     )
#         self.conn.commit()


#     def get(self,id:int)-> dict[str:Any]| None:
#             self.cur.execute("""
#                 SELECT * FROM shipment
#                 WHERE id=?
#             """,(id,))
#             row=self.cur.fetchone()
#             if row is None:
#                 return None

#             return {
#                 "id":row[0],
#                 "content":row[1],
#                 "weight": row[2],
#                 "status": row[3],
                
#             }
    
#     def update(self,id:int,shipment:ShipmentUpdate)-> dict[str:Any]:
#             self.cur.execute("""
#             UPDATE shipment SET status = :status
#             WHERE id = :id
#             """,           {
#                 "id": id,
#                 **shipment.model_dump(),

#             }
#             )
#             self.conn.commit()

#     def delete(self,id:int):
#             self.cur.execute("DELETE FROM shipment WHERE id = ?",(id,))
#             self.conn.commit()


#     def close(self):
#             self.conn.close()