
import numpy as np
import sqlite3 as sql_db


conn_db = sql_db.connect('database.db', check_same_thread=False)
cursor = conn_db.cursor()

def create_table():
    print("Creating Tables ...")
    cursor.execute('''CREATE TABLE IF NOT EXISTS members
        (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            index_num TEXT NOT NULL, 
            course TEXT NOT NULL,
            img_encoding BLOB NOT NULL
        )
    ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS attendace
        (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            check_in_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn_db.commit()
    
    print("Tables created successfully.")
    

def insert_face(name, index_num, course, img_encoding):
    print("Adding Student...")
    insert = cursor.execute("INSERT INTO members (name,index_num,course,img_encoding) VALUES (?,?,?,?)", (name,index_num, course, img_encoding))

    if insert.rowcount > 0:
        # print(f"Face for '{name}' added successfully.")
        conn_db.commit()

        return True
    
    else:
        return False
    
    

def check_in(name, index_num, course, img_encoding):
    print("Adding Student...")
    cursor.execute("INSERT INTO attendace (name,index_num) VALUES (?,?)", (name,index_num))
    conn_db.commit()
    print(f"Face for '{name}' Added successfully.")
    

def delete_face(name):
    cursor.execute("DELETE FROM members WHERE name=?", (name,))
    conn_db.commit()
    print(f"Face for '{name}' deleted successfully.")
    

def update_face(name, new_name):
    cursor.execute("UPDATE members SET name=? WHERE name=?", (new_name, name))
    conn_db.commit()
    print(f"Face for '{name}' updated to '{new_name}' successfully.")
    

def get_face_encoding(name):
    cursor.execute("SELECT img_encoding FROM members WHERE name=?", (name,))
    row = cursor.fetchone()
    if row:
        encoding = np.frombuffer(row[0], dtype=np.float64)
        return encoding
    else:
        return None
    


def load_known_faces():

    known_names = []
    index_nums = []
    known_names_img_encodings = []
    
    cursor.execute("SELECT name, index_num, img_encoding FROM members")
    rows = cursor.fetchall()
    for row in rows:
        known_names.append(row[0])
        index_nums.append(row[1])
        encoding = np.frombuffer(row[2], dtype=np.float64)
        known_names_img_encodings.append(encoding)

    return known_names, index_nums, known_names_img_encodings