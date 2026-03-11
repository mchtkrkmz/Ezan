import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print("Downloading TR cities...")
try:
    req = urllib.request.urlopen('https://raw.githubusercontent.com/enisbt/turkey-cities/master/cities.json', context=ctx)
    tr_data = json.loads(req.read())
except Exception as e:
    print("Error TR:", e)
    tr_data = []

print("Downloading Capitals...")
try:
    req = urllib.request.urlopen('https://raw.githubusercontent.com/Stefie/geojson-world/master/capitals.geojson', context=ctx)
    caps_data = json.loads(req.read())
except Exception as e:
    print("Error CAPS:", e)
    caps_data = {"features": []}

cities = []
for c in tr_data:
    cities.append({
        'lat': float(c['latitude']),
        'lng': float(c['longitude']),
        'city': c['name'],
        'country': 'Türkiye',
        'tz': 'Europe/Istanbul'
    })

for f in caps_data.get('features', []):
    props = f.get('properties', {})
    geom = f.get('geometry', {})
    if props and geom and props.get('city') != 'Ankara':  # prevent duplicate
        coords = geom.get('coordinates', [0,0])
        cities.append({
            'lat': float(coords[1]),
            'lng': float(coords[0]),
            'city': props.get('city'),
            'country': props.get('country', 'Bilinmiyor'),
            'tz': 'UTC' # Generic, will be converted via TSİ anyway in UI
        })

out = json.dumps(cities, indent=4)
with open('cities_array.json', 'w', encoding='utf-8') as f:
    f.write(out)

print("Saved", len(cities), "cities.")
