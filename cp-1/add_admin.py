import sqlite3

DB_PATH = r"D:\cp-1\database.db"
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
          ("Admin", "admin@spam.com", "admin", "admin"))

conn.commit()
conn.close()
print("✅ Admin account created successfully!")
