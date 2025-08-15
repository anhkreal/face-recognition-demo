/**
 * API Utilities Module
 * Handles API calls and authentication
 */

/**
 * A generic function to call protected API endpoints (requires authentication).
 */
function callProtectedApi(endpoint, options, resultId, successMessage, useGlobalLoading = false) {
  if (useGlobalLoading && window.showGlobalLoading) {
    window.showGlobalLoading();
  } else {
    window.UIUtils.showLoading(resultId, true);
  }
  
  // Add token to headers for authentication
  const token = sessionStorage.getItem('authToken');
  
  if (!token || token === 'undefined' || token === 'null') {
    alert('Token không hợp lệ! Vui lòng đăng nhập lại.');
    window.location.href = 'auth.html';
    return;
  }
  
  const authHeader = `Bearer ${token}`;
  
  const fetchOptions = {
    ...options,
    headers: {
      ...(options.headers || {}),
      'Authorization': authHeader
    }
  };
  
  fetch(`${window.API_CONFIG.host}/${endpoint}`, fetchOptions)
    .then(res => {
      if (!res.ok) {
        return res.text().then(text => { throw new Error(`HTTP error! status: ${res.status}, message: ${text}`) });
      }
      return res.json();
    })
    .then(data => {
      if (useGlobalLoading && window.hideGlobalLoading) {
        window.hideGlobalLoading();
      }
      window.UIUtils.showApiResult(resultId, data, successMessage);
    })
    .catch(err => {
      if (useGlobalLoading && window.hideGlobalLoading) {
        window.hideGlobalLoading();
      }
      window.UIUtils.showApiResult(resultId, { error: err.message || String(err) });
    });
}

/**
 * A generic function to call public API endpoints (no authentication required).
 */
function callApi(endpoint, options, resultId, successMessage, useGlobalLoading = false) {
  if (useGlobalLoading && window.showGlobalLoading) {
    window.showGlobalLoading();
  } else {
    window.UIUtils.showLoading(resultId, true);
  }
  
  fetch(`${window.API_CONFIG.host}/${endpoint}`, options)
    .then(res => {
      if (!res.ok) {
        return res.text().then(text => { throw new Error(`HTTP error! status: ${res.status}, message: ${text}`) });
      }
      return res.json();
    })
    .then(data => {
      if (useGlobalLoading && window.hideGlobalLoading) {
        window.hideGlobalLoading();
      }
      window.UIUtils.showApiResult(resultId, data, successMessage);
    })
    .catch(err => {
      if (useGlobalLoading && window.hideGlobalLoading) {
        window.hideGlobalLoading();
      }
      window.UIUtils.showApiResult(resultId, { error: err.message || String(err) });
    });
}

// Export to global scope
window.APIUtils = {
  callProtectedApi,
  callApi
};
