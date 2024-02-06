import sqlite3
import json
import codecs

conn = sqlite3.connect('location_data.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Locations')
fhand = codecs.open('coordinates.js', mode='w', encoding='utf-8')


