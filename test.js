
const aptTime = new Date("2026-08-25T15:00:00Z");
const slotDate = new Date("2026-08-25T12:00:00-03:00");
console.log(aptTime.getTime() === slotDate.getTime());
