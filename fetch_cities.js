const fs = require('fs');
const https = require('https');

function download(url) {
    return new Promise((resolve, reject) => {
        https.get(url, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => resolve(JSON.parse(data)));
        }).on('error', reject);
    });
}

async function run() {
    try {
        console.log("Downloading world cities...");
        // https://raw.githubusercontent.com/lutangar/cities.json/master/cities.json handles big amount, but could be too large
        // Let's get a smaller list: capitals
        const worldData = await download('https://raw.githubusercontent.com/steveflen/country-capitals/master/country-capitals.json');

        console.log("Downloading TR cities...");
        // TR provinces list:
        const trData = await download('https://gist.githubusercontent.com/ozdemirburak/4821a26ea78a7242a510CE8ff2d0571c/raw/0ec2d8a5eb6fa85bca3a8c16053f3dd61ca20af5/cities_of_turkey.json');

        const finalCities = [];

        // Add TR cities
        for (const c of trData) {
            finalCities.push({
                lat: parseFloat(c.latitude),
                lng: parseFloat(c.longitude),
                city: c.name,
                country: 'Türkiye',
                tz: 'Europe/Istanbul'
            });
        }

        // Add world capitals
        for (const c of worldData) {
            if (c.CapitalName && c.CapitalLatitude && c.CapitalLongitude) {
                // Skip if already added (like Ankara)
                if (c.CountryName === 'Turkey') continue;

                finalCities.push({
                    lat: parseFloat(c.CapitalLatitude),
                    lng: parseFloat(c.CapitalLongitude),
                    city: c.CapitalName,
                    country: c.CountryName,
                    tz: c.ContinentName === 'Europe' ? 'Europe/London' : 'UTC' // We'll just use UTC or similar, Adhan.js calculates times using coordinates anyway, TSİ is derived globally now. Actuall timezone is only needed if we want local times. But we show local time inside tooltip, which we actually removed or changed to TSİ! We changed local time to TSİ in tooltip! So tz field is practically unused now!
                });
            }
        }

        fs.writeFileSync('cities_array.json', JSON.stringify(finalCities, null, 2));
        console.log(`Saved ${finalCities.length} cities.`);
    } catch (e) {
        console.error(e);
    }
}
run();
