"""
import psycopg2
=======
'''import psycopg2
>>>>>>> 3b886fb0ba6f6498fa45a69fa30c56d3c7798f0e
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
    print "Connected!\n"

    cursor.execute("SELECT * FROM Problems")

    rows = cursor.fetchall()

    for row in rows:
        print row

    print"\n"

    cursor.execute("SELECT * FROM auth_user")

    rows = cursor.fetchall()

    for row in rows:
        print row
        print"\n"

except:
    print "Failed to Connect!\n"

finally:
    if conn:
        conn.close()	 
"""
