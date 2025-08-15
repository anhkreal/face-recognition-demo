/**
 * Navigation Component
 * Handles authentication navigation and user interface
 */

function renderAuthNav() {
  const authNavArea = document.getElementById('authNavArea');
  if (!authNavArea) return;
  
  authNavArea.innerHTML = '';
  const username = sessionStorage.getItem('username');
  const isLoggedIn = sessionStorage.getItem('isLoggedIn') === 'true';
  
  if (isLoggedIn && username) {
    // Hiển thị username và nút đăng xuất
    const userSpan = document.createElement('span');
    userSpan.className = 'user-chip px-4 py-2 rounded-lg bg-indigo-50 text-indigo-700 font-semibold text-sm flex items-center gap-2';
    userSpan.innerHTML = `<i class="fa-solid fa-user"></i> ${username}`;

    const logoutBtn = document.createElement('button');
    logoutBtn.className = 'logout-btn px-4 py-2 rounded-lg bg-indigo-500 hover:bg-indigo-600 text-white font-semibold text-sm transition flex items-center gap-2';
    logoutBtn.innerHTML = '<i class="fa-solid fa-right-from-bracket"></i>';
    logoutBtn.title = 'Đăng xuất';
    logoutBtn.onclick = function() {
      // Add click animation effect
      logoutBtn.style.transform = 'scale(0.95)';
      setTimeout(() => {
        logoutBtn.style.transform = '';
      }, 150);
      
      // Show confirmation with animation
      if (confirm('Bạn có chắc chắn muốn đăng xuất?')) {
        // Add logout animation
        logoutBtn.style.opacity = '0.5';
        logoutBtn.style.transform = 'scale(0.9) rotate(360deg)';
        
        setTimeout(() => {
          sessionStorage.removeItem('username');
          sessionStorage.removeItem('isLoggedIn');
          sessionStorage.removeItem('authToken');
          renderAuthNav();
        }, 300);
      }
    };

    authNavArea.appendChild(userSpan);
    authNavArea.appendChild(logoutBtn);
  } else {
    // Hiển thị nút đăng nhập
    const loginBtn = document.createElement('button');
    loginBtn.className = 'login-btn px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm transition flex items-center gap-2';
    loginBtn.id = 'loginNavBtn';
    loginBtn.innerHTML = '<i class="fa-solid fa-right-to-bracket"></i> Login';
    loginBtn.onclick = function() {
      window.location.href = 'auth.html';
    };

    authNavArea.appendChild(loginBtn);
  }
}

// Export to global scope
window.Navigation = {
  renderAuthNav
};
