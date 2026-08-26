const API_URL = "http://127.0.0.1:8000";

async function login(email, password) {
    try {
        const response = await fetch(`${API_URL}/login/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });
        if (!response.ok) return false;
        const data = await response.json();
        localStorage.setItem("access_token", data.access_token);
        return true;
    } catch (error) {
        console.error(error);
        return false;
    }
}

async function getMe() {
    const token = localStorage.getItem("access_token");
    if (!token) return null;
    try {
        const response = await fetch(`${API_URL}/users/me`, {
            method: "GET",
            headers: { "Authorization": `Bearer ${token}` }
        });
        if (response.status === 401) { logout(); return null; }
        return await response.json();
    } catch (error) { return null; }
}

async function getNutritionists() {
    const token = localStorage.getItem("access_token");
    const res = await fetch(`${API_URL}/nutritionists/`, { headers: { "Authorization": `Bearer ${token}` }});
    return await res.json();
}

async function getAppointments(nutritionistId = null) {
    const token = localStorage.getItem("access_token");
    let url = `${API_URL}/appointment/`;
    if (nutritionistId) url += `?nutritionist_id=${nutritionistId}`;
    const res = await fetch(url, { headers: { "Authorization": `Bearer ${token}` }});
    return await res.json();
}

async function createAppointment(data) {
    const token = localStorage.getItem("access_token");
    const res = await fetch(`${API_URL}/appointment/`, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
        body: JSON.stringify(data)
    });
    return res.ok;
}

async function deleteAppointment(id) {
    const token = localStorage.getItem("access_token");
    const res = await fetch(`${API_URL}/appointment/${id}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${token}` }
    });
    return res.ok;
}

function logout() {
    localStorage.removeItem("access_token");
    window.location.href = "index.html";
}
