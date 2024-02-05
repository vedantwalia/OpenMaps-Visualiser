import urllib.request, urllib.parse, urllib.error
import sqlite3
import ssl
import json
import time

service_url = 'https://py4e-data.dr-chuck.net/opengeo?'



conn = sqlite3.connect('location_data.sqlite')
cur = conn.cursor()

#Since Python does not have any signed certificates inbuilt, to mitigate the potential errors

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


cur.execute('CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)')

fh = open("where.data") #pulling the crowdsourced list of colleges
count = 0

for line in fh:
    if count > 200:
        print(f'Pulled 200 results, please restart to get more')
        break

    address = line.strip()
    
    cur.execute('SELECT geodata from Locations Where address = ? ', (memoryview(address.encode()), ))
    
    # checking for already reterived results
    try:
        data = cur.fetchone()[0] 
        print(f'Found in database, {address}') 
        continue
    
    except:
        pass

    parms = dict()
    parms['q'] = address
    encoded = urllib.parse.urlencode(parms)
    
    url = f"{service_url}{encoded}"

    print(f'Reteriving {url}')

    uh = urllib.request.urlopen(url, context=ctx)
    data = uh.read().decode()
    #print(f"Reterived {len(data)} characters {data[:20].replace('\n', '')}")
    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))
    count += 1

    try:
        js = json.loads(data)
    except:
        print(data) #incase of any errors we stop the program to read the output
        continue
    if not js or 'features' not in js:
        print('==== Download error ===')
        print(data)
        break

    if len(js['features']) == 0:
        print('==== Object not found ====')
        nofound = nofound + 1

    cur.execute('''INSERT INTO Locations (address, geodata)
                VALUES ( ? , ? )''', (memoryview(address.encode()), memoryview(data.encode()) ) )
    conn.commit()

    if count % 10 == 0 :
        print('Pausing for a bit...')
        time.sleep(5)