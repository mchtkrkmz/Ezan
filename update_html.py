import json

# Read the generated cities
with open('cities_array.json', 'r', encoding='utf-8') as f:
    cities = json.load(f)

# Filter null cities
valid_cities = [c for c in cities if c.get('city')]

# Create the JS code
cities_js = "const CITIES = " + json.dumps(valid_cities, ensure_ascii=False, indent=4) + ";"

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the CITIES block and replace
start_idx = html.find('const CITIES = [')
if start_idx == -1:
    print("Could not find start index")
    exit(1)

end_idx = html.find('];', start_idx)
if end_idx == -1:
    print("Could not find end index")
    exit(1)

# we must find the start of the line or just replace exactly
new_html = html[:start_idx] + cities_js + html[end_idx+2:]

# Also fix the JS bug with timeForPrayer('none')
js_replacement = """                // Sonraki ezan vaktini hesapla
                if (cd.times && cd.times.raw) {
                    let next = cd.times.raw.nextPrayer();
                    let nextTime = cd.times.raw.timeForPrayer(next);
                    
                    if (next === 'none' || !nextTime) {
                        const tomorrow = new Date(now.getTime() + 24 * 60 * 60 * 1000);
                        const tmrwTimes = calcPrayerTimes(cd.lat, cd.lng, tomorrow);
                        if (tmrwTimes && tmrwTimes.raw) {
                            next = 'fajr';
                            nextTime = tmrwTimes.raw.timeForPrayer('fajr');
                        }
                    }

                    cd.nextPrayerName = (next !== 'none' && PRAYER_INFO[next]) ? PRAYER_INFO[next].name : '-';
                    cd.nextPrayerTime = nextTime;
                }"""

old_buggy_code = """                // Sonraki ezan vaktini hesapla
                if (cd.times && cd.times.raw) {
                    const next = cd.times.raw.nextPrayer();
                    const nextTime = cd.times.raw.timeForPrayer(next);
                    cd.nextPrayerName = (next !== 'none' && PRAYER_INFO[next]) ? PRAYER_INFO[next].name : '-';
                    cd.nextPrayerTime = nextTime;
                }"""

new_html = new_html.replace(old_buggy_code, js_replacement)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("index.html updated successfully!")
