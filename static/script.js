async function login() {
    const email = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // FastAPI Users /auth/jwt/login expects form data by default
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const response = await fetch('/auth/jwt/register', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        loadAppointments();
    } else {
        alert('Login failed');
    }
}

async function loadAppointments() {
    const token = localStorage.getItem('token');
    const response = await fetch('/appointments', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const appointments = await response.json();
    const list = document.getElementById('appointments');
    list.innerHTML = appointments.map(a => `<li>${a.date} - ${a.patient_name}</li>`).join('');
}

function updateUI() {
    const token = localStorage.getItem('token');
    if (token) {
        document.getElementById('login-form').classList.add('hidden');
        document.getElementById('appointments').classList.remove('hidden');
    } else {
        document.getElementById('login-form').classList.remove('hidden');
        document.getElementById('appointments').classList.add('hidden');
    }
}

async function register() {
    // 1. Capture inputs
    const fullName = document.getElementById('reg-fullname').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;

    // 2. Validate inputs locally
    if (!fullName || !email || !password) {
        alert("Please fill in all fields");
        return;
    }

    // 3. Prepare payload matching your UserCreate schema
    const payload = {
        email: email,
        password: password,
        full_name: fullName,
        is_active: true,
        is_superuser: false,
        is_verified: false
    };

    try {
        const response = await fetch('/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            alert('Registration successful! You can now log in.');
            // After successful registration, you could redirect to a login page 
            // or automatically trigger the login flow.
        } else {
            const errorData = await response.json();
            alert(`Registration failed: ${JSON.stringify(errorData.detail)}`);
        }
    } catch (error) {
        console.error('Connection Error:', error);
        alert('Could not connect to the server.');
    }
}