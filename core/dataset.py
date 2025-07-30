import sqlite3
import os
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "../userData/rolls.sqlite")

connection = sqlite3.connect(db_path)

c = connection.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS full_roll(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stat TEXT,
    percentage REAL,
    valid INTEGER
    )""")

def table_add(roll):
    for i, stat in enumerate(roll.list):
        c.execute( "INSERT INTO full_roll (stat, percentage, valid) VALUES (?, ?, ?)",
            (stat.stat, stat.getNum(), roll.valid[i]))
        
    connection.commit()
    
def view_table():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for row in cursor.execute("SELECT * FROM full_roll"):
        print(row)
    
    conn.close() 

view_table()