import sqlite3
import os

db_path = r"c:\Users\Wesley\Desktop\meu jogo 3d 3 os assets\🌍 MYTHARA Gurra de Raças 17-10-2025\Server\gamedata.db"
if not os.path.exists(db_path):
    print('DB not found:', db_path)
else:
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
    for name, sql in cur.fetchall():
        print('TABLE:', name)
        # print('SQL:', sql)
    con.close()
