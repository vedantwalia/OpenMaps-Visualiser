import sqlite3
import json
import codecs

conn = sqlite3.connect('location_data.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Locations')
count = 0
fhand = codecs.open('where.js', mode='w', encoding='utf-8')
fhand.write("Coordinates = [\n")

for row in cur:
    data = str(row[1].decode())
    try:
        js = json.loads(str(data))
    except:
        continue
    
    if len(js['features']) == 0:
        continue
    try:
        lat = js['features'][0]['geometry']['coordinates'][1]
        lng = js['features'][0]['geometry']['coordinates'][0]
        where = js['features'][0]['properties']['display_name']
        where = where.replace("'", "")
    except:
        print(f'Unexpected format!')
        print(js)
    
    try:
        print(f"{where} {lat} {lng}")
        count = count + 1
        if count > 1:
            fhand.write(',\n')
            output = f"[{lat},{lng}, '{where}']"
            fhand.write(output)
        
    except:
        continue

fhand.write("\n]; \n")
cur.close()
fhand.close()
print(f'{count} records writen to where.js')