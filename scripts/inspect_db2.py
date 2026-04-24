import sqlite3
import os

db_path = r"c:\Users\Wesley\Desktop\meu jogo 3d 3 os assets\🌍 MYTHARA Gurra de Raças 17-10-2025\Server\resources\gamedata.db"
if not os.path.exists(db_path):
    print('DB not found:', db_path)
else:
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [r[0] for r in cur.fetchall()]
    print('Tables:')
    for t in tables:
        print(' -', t)
    # Inspect some candidate tables
    candidates = ['PlayerVariables','UserVariables','ServerVariables']
    for candidate in candidates:
        if candidate in tables:
            print(f"\nSchema for {candidate}:")
            cur.execute(f"PRAGMA table_info({candidate});")
            for col in cur.fetchall():
                print('  ', col)
            print(f"\nSome rows from {candidate}:")
            cur.execute(f"SELECT * FROM {candidate} LIMIT 10")
            for row in cur.fetchall():
                print('  ', row)
    con.close()
