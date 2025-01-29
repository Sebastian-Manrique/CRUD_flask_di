import sqlite3
con = sqlite3.connect("usuarios.db")
cur = con.cursor()

cur.execute("""
    INSERT INTO usuarios VALUES
        (001, 'sebastianmanriquemontiel@gmail.com', 'prueba')
""")

res = cur.execute("SELECT name FROM sqlite_master")
res.fetchone()
print(res.fetchone())