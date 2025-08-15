/**
 * Reset Module
 * Handles resetting the entire system index
 * Copied from frontend-v3/utils/main.js
 */

function callReset() {
  callProtectedApi('reset_index', { method: 'POST' }, 'resetResult', 'Reset index thành công!', true);
}

// Legacy wrapper function for backward compatibility
function callResetDatabase() {
  callReset();
}

// Make functions globally available
window.callReset = callReset;
window.callResetDatabase = callResetDatabase;