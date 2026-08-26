let currentUser = null;
let selectedNutriId = null;
let selectedDate = null;
let selectedTime = null;
let currentNutriAppointments = [];
let agendaDate = new Date();

const DIAS_SEMANA = ['Domingo', 'Segunda-feira', 'Terca-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sabado'];

document.addEventListener('DOMContentLoaded', async () => {
    currentUser = await getMe();
    if (!currentUser) return;
    
    document.getElementById('user-role-badge').textContent = currentUser.role;

    if (currentUser.role === 'PATIENT') {
        document.getElementById('menu-agendar').style.display = 'block';
        loadNutritionists();
    } else {
        document.getElementById('menu-bloquear').style.display = 'block';
    }

    loadAgenda();
});

function showView(viewId) {
    document.querySelectorAll('.view-section').forEach(v => v.classList.remove('active'));
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    document.getElementById('view-' + viewId).classList.add('active');
    if (event && event.target) event.target.classList.add('active');
    if (viewId === 'agenda') loadAgenda();
}

function changeAgendaDay(delta) {
    agendaDate.setDate(agendaDate.getDate() + delta);
    loadAgenda();
}

function getLocalDateStr(d) {
    var y = d.getFullYear();
    var m = (d.getMonth() + 1).toString().padStart(2, '0');
    var day = d.getDate().toString().padStart(2, '0');
    return y + '-' + m + '-' + day;
}

function parseAptTime(startTime) {
    var str = (startTime && startTime.endsWith && startTime.endsWith("Z")) ? startTime : startTime + "Z";
    return new Date(str);
}

async function loadAgenda() {
    var grid = document.getElementById('agenda-grid');
    var label = document.getElementById('agenda-day-label');
    grid.innerHTML = '';

    var dateStr = getLocalDateStr(agendaDate);
    var diaSemana = DIAS_SEMANA[agendaDate.getDay()];
    var dia = agendaDate.getDate().toString().padStart(2, '0');
    var mes = (agendaDate.getMonth() + 1).toString().padStart(2, '0');
    label.textContent = diaSemana + ', ' + dia + '/' + mes + '/' + agendaDate.getFullYear();

    var appointments = await getAppointments();

    var parts = dateStr.split('-');
    var year = parseInt(parts[0]);
    var month = parseInt(parts[1]) - 1;
    var day = parseInt(parts[2]);

    for (var i = 8; i <= 17; i++) {
        for (var j = 0; j < 60; j += 30) {
            var hourStr = i.toString().padStart(2, '0') + ':' + j.toString().padStart(2, '0');
            var slotDate = new Date(year, month, day, i, j);

            var apt = null;
            for (var k = 0; k < appointments.length; k++) {
                if (parseAptTime(appointments[k].start_time).getTime() === slotDate.getTime()) {
                    apt = appointments[k];
                    break;
                }
            }

            var slot = document.createElement('div');

            if (apt) {
                if (apt.status === 'blocked') {
                    slot.className = 'agenda-slot slot-blocked';
                    slot.innerHTML = '<span class="slot-hora">' + hourStr + '</span>' +
                        '<span class="slot-status">Bloqueado</span>' +
                        '<button class="slot-cancel-btn" onclick="cancelarConsulta(' + apt.id + ')">Desbloquear</button>';
                } else {
                    var info = currentUser.role === 'PATIENT' ?
                        'Nutri #' + apt.nutritionist_id :
                        (apt.patient_id ? 'Paciente #' + apt.patient_id : 'Reservado');
                    slot.className = 'agenda-slot slot-booked';
                    slot.innerHTML = '<span class="slot-hora">' + hourStr + '</span>' +
                        '<span class="slot-status">' + info + '</span>' +
                        '<button class="slot-cancel-btn" onclick="cancelarConsulta(' + apt.id + ')">Cancelar</button>';
                }
            } else {
                slot.className = 'agenda-slot slot-livre';
                slot.innerHTML = '<span class="slot-hora">' + hourStr + '</span>' +
                    '<span class="slot-status">Livre</span>';
            }

            grid.appendChild(slot);
        }
    }
}

async function cancelarConsulta(id) {
    if (confirm('Tem certeza que deseja cancelar?')) {
        await deleteAppointment(id);
        loadAgenda();
    }
}

// --------- PACIENTE FLOW ---------
async function loadNutritionists() {
    var select = document.getElementById('nutri-select');
    var nutris = await getNutritionists();
    for (var k = 0; k < nutris.length; k++) {
        var n = nutris[k];
        var opt = document.createElement('option');
        opt.value = n.id;
        opt.textContent = n.name + ' (' + n.specialty + ')';
        select.appendChild(opt);
    }
}

async function loadNutriSchedule() {
    selectedNutriId = document.getElementById('nutri-select').value;
    if (!selectedNutriId) {
        document.getElementById('schedule-picker').style.display = 'none';
        return;
    }
    document.getElementById('schedule-picker').style.display = 'block';
    currentNutriAppointments = await getAppointments(selectedNutriId);

    var today = getLocalDateStr(new Date());
    document.getElementById('schedule-date').min = today;
    renderTimeSlots();
}

function renderTimeSlots() {
    selectedDate = document.getElementById('schedule-date').value;
    var container = document.getElementById('time-slots');
    var btn = document.getElementById('btn-confirm-agendamento');
    btn.disabled = true;
    selectedTime = null;

    if (!selectedDate) { container.innerHTML = ''; return; }

    container.innerHTML = '';

    var parts = selectedDate.split('-');
    var year = parseInt(parts[0]);
    var month = parseInt(parts[1]) - 1;
    var day = parseInt(parts[2]);

    for (var i = 8; i <= 17; i++) {
        for (var j = 0; j < 60; j += 30) {
            var hourStr = i.toString().padStart(2, '0') + ':' + j.toString().padStart(2, '0');
            var slotDate = new Date(year, month, day, i, j);

            var isTaken = false;
            for (var k = 0; k < currentNutriAppointments.length; k++) {
                if (parseAptTime(currentNutriAppointments[k].start_time).getTime() === slotDate.getTime()) {
                    isTaken = true;
                    break;
                }
            }

            var slot = document.createElement('div');
            slot.className = 'time-slot' + (isTaken ? ' disabled' : '');
            slot.textContent = isTaken ? hourStr + ' (Ocupado)' : hourStr;

            if (!isTaken) {
                (function(h) {
                    slot.onclick = function() {
                        var all = document.querySelectorAll('.time-slot');
                        for (var x = 0; x < all.length; x++) all[x].classList.remove('selected');
                        this.classList.add('selected');
                        selectedTime = h;
                        btn.disabled = false;
                    };
                })(hourStr);
            }
            container.appendChild(slot);
        }
    }
}

async function confirmarAgendamento() {
    if (!selectedNutriId || !selectedDate || !selectedTime) return;

    var parts = selectedDate.split('-');
    var localDate = new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]),
        parseInt(selectedTime.split(':')[0]), parseInt(selectedTime.split(':')[1]));
    var startTime = localDate.toISOString();

    var success = await createAppointment({
        start_time: startTime,
        nutritionist_id: parseInt(selectedNutriId),
        patient_id: currentUser.profile_id,
        status: "booked"
    });

    if (success) {
        alert('Agendamento realizado com sucesso!');
        loadNutriSchedule();
        showView('agenda');
    } else {
        alert('Erro ao agendar. O horario pode ter sido ocupado.');
    }
}

// --------- NUTRICIONISTA FLOW ---------
async function bloquearHorario() {
    var date = document.getElementById('block-date').value;
    var time = document.getElementById('block-time').value;
    if (!date || !time) return alert('Preencha data e hora.');

    var parts = date.split('-');
    var timeParts = time.split(':');
    var localDate = new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]),
        parseInt(timeParts[0]), parseInt(timeParts[1]) || 0);
    var startTime = localDate.toISOString();

    var success = await createAppointment({
        start_time: startTime,
        nutritionist_id: currentUser.profile_id,
        patient_id: null,
        status: "blocked"
    });

    if (success) {
        alert('Horario bloqueado com sucesso!');
        showView('agenda');
    } else {
        alert('Erro ao bloquear horario. Ja existe agendamento neste horario?');
    }
}