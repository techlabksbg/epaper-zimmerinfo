import sqlite3
import random
anzahl = 20

verbindung = sqlite3.connect("test.db")

print(verbindung.total_changes)

cursor = verbindung.cursor()

cursor.execute("DROP TABLE if EXISTS volt")
# cursor.execute("DELETE FROM volt WHERE id = 3")

cursor.execute("CREATE TABLE IF NOT EXISTS volt (id INTEGER PRIMARY KEY, volt REAL, macid INTEGER, time INTEGER)")
# cursor.execute("CREATE TABLE volt (id INTEGER, volt REAL, macid INTEGER, time INTEGER)")

for i in range(anzahl):
    zufallsvolt = 2.5 + 2 * random.random()
    cursor.execute("INSERT INTO volt (volt, macid, time) VALUES (?, 1, ?)", (zufallsvolt, i * 20))
# cursor.execute("INSERT INTO volt (id, volt, macid, time) VALUES (2, 3.55, 1, 10)")
# cursor.execute("INSERT INTO volt (id, volt, macid, time) VALUES (3, 3.05, 1, 20)")
# cursor.execute("INSERT INTO volt (id, volt, macid, time) VALUES (4, 2.05, 1, 30)")

# cursor.execute("INSERT INTO volt (volt, macid, time) VALUES (4.05, 1, 0), (3.55, 1, 10), (3.05, 1, 20), (2.05, 1, 30)")


cursor.execute("UPDATE volt SET volt = ? WHERE id = ?", (3.2, 4))


verbindung.commit()


cursor.execute("SELECT * FROM volt")
inhalt_volt = cursor.fetchall()

for zeile in inhalt_volt:
    print(zeile)

print(verbindung.total_changes)

verbindung.close()
