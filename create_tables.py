import sqlite3
connection=sqlite3.connect('data.db')
cursor=connection.cursor()

create_table="CREATE TABLE IF NOT EXISTS info(id int PRIMARY KEY,first_name text,second_name text)"
cursor.execute(create_table)
connection.commit()
connection.close()
