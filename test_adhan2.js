const adhan = require('adhan');
const now = new Date();
// Artificially make now at 23:30
now.setHours(23, 30, 0, 0);
const pt = new adhan.PrayerTimes(new adhan.Coordinates(41.01, 28.97), now, adhan.CalculationMethod.Turkey());
console.log(pt.nextPrayer());
console.log(pt.timeForPrayer(pt.nextPrayer()));
