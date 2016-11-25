"""
=======
'''
>>>>>>> 3b886fb0ba6f6498fa45a69fa30c56d3c7798f0e
import psycopg2
import sys

db_name = "dcf69vk9fp4ss6"
db_user = "xdkiviulaenabi"
db_pw = "Qx2B9JRO_ri6plgVgyo-D9j8ET"
db_host = "ec2-54-225-101-191.compute-1.amazonaws.com"
db_port = 5432

conn = None

try:
    conn = psycopg2.connect(
    database=db_name,
        user=db_user,
        password=db_pw,
        host=db_host,
        port=db_port
    )
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()
    #print "Connected!\n"
    # use cursor to grab version data
    #cursor.execute('SELECT version()')
    #ver = cursor.fetchone()
    #print ver
    # making example table
    cursor.execute("CREATE TABLE Problems(Id INTEGER PRIMARY KEY, Name VARCHAR(20), Bounty INT)")
    cursor.execute("INSERT INTO Problems VALUES(1,'aids',9000)")
    cursor.execute("INSERT INTO Problems VALUES(2,'world_hunger',8000)")
    cursor.execute("INSERT INTO Problems VALUES(3,'isis',10000)")
    cursor.execute("INSERT INTO Problems VALUES(4,'corruption',29000)")
    conn.commit()

except:
    print "Failed to Connect!\n"

finally:
    if conn:
        conn.close()
    print "Disconnected!\n"
"""
