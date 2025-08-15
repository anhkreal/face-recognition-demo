/**
 * Modal Component
 * Handles confirmation dialogs and loading overlays
 */

// Global loading overlay functions
function showGlobalLoading() {
  document.getElementById('globalLoadingOverlay').classList.add('show');
}

function hideGlobalLoading() {
  document.getElementById('globalLoadingOverlay').classList.remove('show');
}

// Confirmation modal functions
function showConfirmModal(message, onConfirm) {
  document.getElementById('confirmMessage').textContent = message;
  document.getElementById('confirmModal').classList.add('show');
  
  const confirmBtn = document.getElementById('confirmOk');
  const cancelBtn = document.getElementById('confirmCancel');
  
  // Remove existing event listeners
  const newConfirmBtn = confirmBtn.cloneNode(true);
  const newCancelBtn = cancelBtn.cloneNode(true);
  confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
  cancelBtn.parentNode.replaceChild(newCancelBtn, cancelBtn);
  
  // Add new event listeners
  newConfirmBtn.addEventListener('click', () => {
    hideConfirmModal();
    if (onConfirm) onConfirm();
  });
  
  newCancelBtn.addEventListener('click', hideConfirmModal);
}

function hideConfirmModal() {
  document.getElementById('confirmModal').classList.remove('show');
}

// Initialize modal close functionality
function initModal() {
  // Close modal when clicking outside
  document.getElementById('confirmModal').addEventListener('click', (e) => {
    if (e.target.id === 'confirmModal') {
      hideConfirmModal();
    }
  });
}

// Export to global scope
window.showGlobalLoading = showGlobalLoading;
window.hideGlobalLoading = hideGlobalLoading;
window.showConfirmModal = showConfirmModal;
window.hideConfirmModal = hideConfirmModal;
window.Modal = {
  init: initModal
};
