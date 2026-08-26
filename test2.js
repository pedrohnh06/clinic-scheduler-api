
const apt_start_time = "2026-08-25T15:00:00"; // from backend
const parsed_apt_date = new Date(apt_start_time.endsWith("Z") ? apt_start_time : apt_start_time + "Z");

// Simulate loop
for(let i=8; i<=17; i++) {
    for(let j=0; j<60; j+=30) {
        const hourStr = i.toString().padStart(2, '0') + ':' + j.toString().padStart(2, '0');
        const slotDate = new Date(`2026-08-25T${hourStr}:00`);
        
        if (parsed_apt_date.getTime() === slotDate.getTime()) {
            console.log(`MATCHED at hourStr: ${hourStr}`);
        }
    }
}
