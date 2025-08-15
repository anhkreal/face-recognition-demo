/**
 * Snackbar Component
 * Handles notification messages
 */

function showSnackbar(message, type = 'info', duration = 3000) {
  const snackbar = document.getElementById('snackbar');
  
  // Icon mapping
  const icons = {
    success: '<i class="fa-solid fa-check-circle"></i>',
    error: '<i class="fa-solid fa-exclamation-circle"></i>',
    warning: '<i class="fa-solid fa-exclamation-triangle"></i>',
    info: '<i class="fa-solid fa-info-circle"></i>'
  };
  
  snackbar.innerHTML = `
    <div style="display: flex; align-items: center; gap: 12px;">
      ${icons[type] || icons.info}
      <span>${message}</span>
    </div>
  `;
  snackbar.className = `snackbar ${type} show`;
  
  setTimeout(() => {
    snackbar.classList.remove('show');
  }, duration);
}

// Export to global scope
window.showSnackbar = showSnackbar;
