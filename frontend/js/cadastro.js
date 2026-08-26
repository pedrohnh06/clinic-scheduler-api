
function switchTab(tab) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    
    if(tab === 'paciente') {
        document.querySelectorAll('.tab-btn')[0].classList.add('active');
        document.getElementById('tab-paciente').classList.add('active');
    } else {
        document.querySelectorAll('.tab-btn')[1].classList.add('active');
        document.getElementById('tab-nutricionista').classList.add('active');
    }
}

async function handleCadastro(e, type) {
    e.preventDefault();
    const btn = e.target.querySelector('button');
    const msg = document.getElementById('cadastro-msg');
    
    btn.disabled = true;
    btn.textContent = 'Aguarde...';
    msg.style.display = 'none';

    let endpoint, payload;

    if (type === 'paciente') {
        endpoint = '/patients/';
        payload = {
            name: document.getElementById('p-name').value,
            email: document.getElementById('p-email').value,
            birth_date: document.getElementById('p-birth').value,
            password: document.getElementById('p-password').value
        };
    } else {
        endpoint = '/nutritionists/';
        payload = {
            name: document.getElementById('n-name').value,
            email: document.getElementById('n-email').value,
            crn: document.getElementById('n-crn').value,
            specialty: document.getElementById('n-specialty').value,
            password: document.getElementById('n-password').value
        };
    }

    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            msg.className = 'alert alert-success';
            msg.textContent = 'Cadastro realizado com sucesso! Redirecionando...';
            msg.style.display = 'block';
            setTimeout(() => { window.location.href = 'index.html'; }, 2000);
        } else {
            const data = await response.json();
            msg.className = 'alert alert-error';
            msg.textContent = 'Erro ao cadastrar: ' + (data.detail || 'Verifique os dados');
            msg.style.display = 'block';
            btn.disabled = false;
            btn.textContent = 'Cadastrar';
        }
    } catch (error) {
        msg.className = 'alert alert-error';
        msg.textContent = 'Erro de conexão com o servidor.';
        msg.style.display = 'block';
        btn.disabled = false;
        btn.textContent = 'Cadastrar';
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('form-paciente').addEventListener('submit', (e) => handleCadastro(e, 'paciente'));
    document.getElementById('form-nutricionista').addEventListener('submit', (e) => handleCadastro(e, 'nutricionista'));
});
