// Modal Logic
const loginModal = document.getElementById('loginModal');
const loginTitle = document.getElementById('loginTitle');
const loginRoleInput = document.getElementById('loginRole');

function openLoginModal(role) {
    if (!loginModal) return; // Prevent error if logic is loaded on another page
    
    loginModal.classList.add('active');
    
    if (role === 'student') {
        loginTitle.textContent = 'Student Login';
        loginRoleInput.value = 'student';
    } else {
        loginTitle.textContent = 'Faculty / Admin Login';
        loginRoleInput.value = 'staff';
    }
}

function closeLoginModal() {
    if (loginModal) loginModal.classList.remove('active');
}

// Close modal when clicking outside
if (loginModal) {
    loginModal.addEventListener('click', (e) => {
        if (e.target === loginModal) {
            closeLoginModal();
        }
    });
}

// Handle Login Form
async function handleLogin(e) {
    e.preventDefault();
    
    const role = loginRoleInput.value;
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password') ? document.getElementById('password').value.trim() : username;
    
    if (username.length < 3) {
        alert("Please enter a valid username/ID");
        return;
    }
    
    try {
        const response = await fetch('/api/auth/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'username': username,
                'password': password
            })
        });

        if (!response.ok) {
            alert('Login failed. Please check your credentials.');
            return;
        }

        const data = await response.json();
        const tokenPayload = JSON.parse(atob(data.access_token.split('.')[1]));
        
        const userRole = tokenPayload.role === 'admin' ? 'Admin' : (tokenPayload.role === 'teacher' ? 'Teacher' : 'Student');
        
        const user = {
            id: tokenPayload.sub,
            role: userRole,
            name: username,
            token: data.access_token
        };
        
        localStorage.setItem('srms_user', JSON.stringify(user));
        window.location.href = 'dashboard.html';
    } catch (err) {
        console.error(err);
        alert('An error occurred during login');
    }
}

// Check logged in state on load
document.addEventListener('DOMContentLoaded', () => {
    const userStr = localStorage.getItem('srms_user');
    const isDashboard = window.location.pathname.endsWith('dashboard.html');
    
    if (userStr) {
        if (!isDashboard) {
            // Uncomment to auto-redirect if already logged in
            // window.location.href = 'dashboard.html';
        } else {
            // We are on dashboard, populate user info
            const user = JSON.parse(userStr);
            document.getElementById('userNameDisplay').textContent = user.name;
            document.getElementById('userRoleDisplay').textContent = user.role;
            
            // Adjust sidebar based on role
            updateSidebarForRole(user.role);
        }
    } else {
        if (isDashboard) {
            // Not logged in, redirect to login
            window.location.href = 'index.html';
        }
    }
});

function logout() {
    localStorage.removeItem('srms_user');
    window.location.href = 'index.html';
}

// Dashboard Dynamic Sidebar & Views
function updateSidebarForRole(role) {
    const sidebarNav = document.getElementById('sidebarNav');
    if (!sidebarNav) return;

    let navHtml = '';

    // Common Nav Items
    navHtml += `<a class="nav-item active" onclick="switchView('dashboard', this)">Dashboard Overview</a>`;

    if (role === 'Admin') {
        navHtml += `
            <a class="nav-item" onclick="switchView('students', this)">Students Management</a>
            <a class="nav-item" onclick="switchView('marks', this)">Marks Entry</a>
            <a class="nav-item" onclick="switchView('system-results', this)">Result Processing</a>
        `;
    } else if (role === 'Teacher') {
        navHtml += `
            <a class="nav-item" onclick="switchView('students', this)">My Students</a>
            <a class="nav-item" onclick="switchView('marks', this)">Marks Entry</a>
            <a class="nav-item" onclick="switchView('system-results', this)">Results Overview</a>
        `;
    } else if (role === 'Student') {
        navHtml += `
            <a class="nav-item" onclick="switchView('student-result', this)">My Result (Current)</a>
            <a class="nav-item" onclick="alert('Viewing past results...')">Academic History</a>
        `;
    }

    sidebarNav.innerHTML = navHtml;
    
    // Default avatar
    const avatarImg = document.getElementById('userAvatar');
    if (avatarImg) {
        const userStr = localStorage.getItem('srms_user');
        const user = JSON.parse(userStr);
        avatarImg.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(user.name)}&background=08bd80&color=fff`;
    }
}

function switchView(viewId, element) {
    // Update active nav item
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => item.classList.remove('active'));
    
    if (element) {
        element.classList.add('active');
        document.getElementById('currentViewTitle').textContent = element.textContent;
    }

    // Hide all views
    const views = document.querySelectorAll('.view-section');
    views.forEach(v => v.classList.remove('active'));

    // Show selected view
    const activeView = document.getElementById(`view-${viewId}`);
    if (activeView) {
        activeView.classList.add('active');
    }
}




