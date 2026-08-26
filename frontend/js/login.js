document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('login-form');
    if(form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const errorDiv = document.getElementById('login-error');
            
            errorDiv.style.display = 'none';
            const btn = e.target.querySelector('button');
            btn.textContent = 'Carregando...';
            btn.disabled = true;

            const success = await login(email, password);
            
            btn.textContent = 'Entrar';
            btn.disabled = false;

            if (success) {
                window.location.href = 'dashboard.html';
            } else {
                errorDiv.style.display = 'block';
            }
        });
    }
});
