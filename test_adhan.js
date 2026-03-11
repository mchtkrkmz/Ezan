const adhan = require('adhan');
console.log(Object.keys(adhan.CalculationMethod));
const params = adhan.CalculationMethod.Turkey ? adhan.CalculationMethod.Turkey() : adhan.CalculationMethod.MuslimWorldLeague();
console.log(params);
