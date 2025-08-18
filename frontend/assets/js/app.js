/**
 * Main Application Module
 * Handles application initialization and coordination with frontend-v3 compatibility
 */

// Debug utilities - available in global scope
window.debugDOM = {
  // Check if element exists
  checkElement: function(id) {
    const element = document.getElementById(id);
    console.log(`Element '${id}': ${element ? 'EXISTS' : 'NOT FOUND'}`);
    if (element) {
      console.log('Element details:', {
        tagName: element.tagName,
        className: element.className,
        innerHTML: element.innerHTML.substring(0, 100) + (element.innerHTML.length > 100 ? '...' : '')
      });
    }
    return element;
  },
  
  // Find similar IDs
  findSimilar: function(partialId) {
    const elements = Array.from(document.querySelectorAll('[id*="' + partialId + '"]'));
    console.log(`Elements containing '${partialId}':`, elements.map(el => ({
      id: el.id,
      tagName: el.tagName,
      className: el.className
    })));
    return elements;
  },
  
  // List all file input related elements
  listFileInputs: function() {
    const fileInputs = Array.from(document.querySelectorAll('input[type="file"]'));
    console.log('File inputs found:');
    fileInputs.forEach(input => {
      console.log(`- ${input.id}: onchange="${input.getAttribute('onchange')}"`);
    });
    
    const fileNameElements = Array.from(document.querySelectorAll('[id*="FileName"], [id*="fileName"]'));
    console.log('File name elements found:');
    fileNameElements.forEach(el => {
      console.log(`- ${el.id} (${el.tagName})`);
    });
  }
};

// Application initialization
document.addEventListener('DOMContentLoaded', function() {
  console.log('[DEBUG] DOM loaded, checking file input elements...');
  if (window.debugDOM) {
    window.debugDOM.listFileInputs();
  }
  
  // Initialize authentication navigation
  if (window.Navigation && window.Navigation.renderAuthNav) {
    window.Navigation.renderAuthNav();
  }
  
  // Set up file input change listeners
  setupFileInputListeners();
  
  // Set up form validation
  setupFormValidation();
  
  // Show initial page (query)
  const queryPage = document.getElementById('query');
  if (queryPage) {
    showPage('query');
  }
  
  // Initialize page visibility based on auth status
  updatePageVisibility();
  
  console.log('Face Recognition App initialized successfully');
});

function setupFileInputListeners() {
  // Query file input
  const queryFileInput = document.getElementById('queryFile');
  if (queryFileInput) {
    queryFileInput.addEventListener('change', function() {
      // Don't use our updateFileName here since HTML already has onchange handler
      // This is just for additional setup if needed
    });
  }
  
  // Predict file input  
  const predictFileInput = document.getElementById('predictFile');
  if (predictFileInput) {
    predictFileInput.addEventListener('change', function() {
      // Don't use our updateFileName here since HTML might have onchange handler
    });
  }
  
  // Add image file input
  const addImageFileInput = document.getElementById('addImageFile');
  if (addImageFileInput) {
    addImageFileInput.addEventListener('change', function() {
      // Don't use our updateFileName here since HTML might have onchange handler
    });
  }
}

function setupFormValidation() {
  // Real-time validation for age inputs
  const ageInputs = document.querySelectorAll('input[type="number"][id*="uoi"], input[type="number"][id*="age"]');
  ageInputs.forEach(input => {
    input.addEventListener('input', function() {
      const value = this.value.trim();
      if (value && window.Validation && !window.Validation.validateAge(value)) {
        this.setCustomValidity('Tuổi phải là số nguyên dương từ 1 đến 150');
      } else {
        this.setCustomValidity('');
      }
    });
  });
  
  // Real-time validation for ID inputs
  const idInputs = document.querySelectorAll('input[id*="Id"], input[id*="ID"]');
  idInputs.forEach(input => {
    input.addEventListener('input', function() {
      // Simply clear custom validity as the validation is handled by individual functions
      this.setCustomValidity('');
    });
  });
  
  // Real-time validation for class ID inputs
  const classIdInputs = document.querySelectorAll('input[id*="ClassId"], input[id*="classId"]');
  classIdInputs.forEach(input => {
    input.addEventListener('input', function() {
      const value = this.value.trim();
      if (value && window.Validation && !window.Validation.validateClassId(value)) {
        this.setCustomValidity('Class ID phải là số nguyên không âm');
      } else {
        this.setCustomValidity('');
      }
    });
  });
}

function updatePageVisibility() {
  const isLoggedIn = (window.APIUtils && window.APIUtils.isLoggedIn && window.APIUtils.isLoggedIn()) ||
                     sessionStorage.getItem('isLoggedIn') === 'true';
  
  const protectedPages = ['add', 'edit', 'delete', 'search', 'reset'];
  
  protectedPages.forEach(pageId => {
    const pageElement = document.getElementById(pageId);
    const navButton = document.querySelector(`[onclick="showPage('${pageId}')"]`);
    
    if (pageElement) {
      if (isLoggedIn) {
        pageElement.style.display = 'block';
      } else {
        pageElement.style.display = 'none';
      }
    }
    
    if (navButton) {
      if (isLoggedIn) {
        navButton.style.display = 'inline-block';
        navButton.disabled = false;
      } else {
        navButton.style.display = 'none';
        navButton.disabled = true;
      }
    }
  });
  
  // Update navigation visibility
  if (window.Navigation && window.Navigation.renderAuthNav) {
    window.Navigation.renderAuthNav();
  }
}

// Global event handlers for legacy compatibility
function showPage(pageId) {
  // Hide all pages
  const pages = document.querySelectorAll('.page');
  pages.forEach(page => {
    page.classList.remove('active');
    page.style.display = 'none';
  });
  
  // Show selected page
  const selectedPage = document.getElementById(pageId);
  if (selectedPage) {
    selectedPage.style.display = 'block';
    selectedPage.classList.add('active');
  }
  
  // Update tab buttons
  const tabButtons = document.querySelectorAll('.tab-btn');
  tabButtons.forEach(btn => {
    btn.classList.remove('active');
  });
  
  const activeButton = document.querySelector(`[onclick="showPage('${pageId}')"]`);
  if (activeButton) {
    activeButton.classList.add('active');
  }
  
  // Use UIUtils if available
  if (window.UIUtils && window.UIUtils.showPage) {
    window.UIUtils.showPage(pageId);
  }
}

function logout() {
  if (window.Navigation && window.Navigation.logout) {
    window.Navigation.logout();
  } else {
    // Fallback logout
    sessionStorage.removeItem('isLoggedIn');
    sessionStorage.removeItem('username');
    sessionStorage.removeItem('authToken');
    updatePageVisibility();
    showPage('query');
    if (window.showSnackbar) {
      window.showSnackbar('Đã đăng xuất thành công!', 'success');
    }
  }
}

// Query page functions
function callQuery() {
  if (window.QueryPage && window.QueryPage.callQuery) {
    window.QueryPage.callQuery();
  }
}

// Predict page functions
function callPredict() {
  if (window.PredictPage && window.PredictPage.callPredict) {
    window.PredictPage.callPredict();
  }
}

// Add page functions
function callAddNguoi() {
  if (window.AddPersonPage && window.AddPersonPage.callAddNguoi) {
    window.AddPersonPage.callAddNguoi();
  }
}

function callAddImage() {
  if (window.AddPersonPage && window.AddPersonPage.callAddImage) {
    window.AddPersonPage.callAddImage();
  }
}

// Edit page functions
function callEditNguoi() {
  if (window.EditPersonPage && window.EditPersonPage.callEditNguoi) {
    window.EditPersonPage.callEditNguoi();
  }
}

function callGetNguoi() {
  if (window.EditPersonPage && window.EditPersonPage.callGetNguoi) {
    window.EditPersonPage.callGetNguoi();
  }
}

// Delete page functions
function callDeleteNguoi() {
  if (window.DeletePersonPage && window.DeletePersonPage.callDeleteNguoi) {
    window.DeletePersonPage.callDeleteNguoi();
  }
}

function callDeleteImage() {
  if (window.DeletePersonPage && window.DeletePersonPage.callDeleteImage) {
    window.DeletePersonPage.callDeleteImage();
  }
}

// Search page functions
function callSearchNguoi(page = 1) {
  if (window.SearchPage && window.SearchPage.callSearchNguoi) {
    window.SearchPage.callSearchNguoi(page);
  }
}

function callGetAllNguoi(page = 1, sortBy = 'ten_asc') {
  if (window.SearchPage && window.SearchPage.callGetAllNguoi) {
    window.SearchPage.callGetAllNguoi(page, sortBy);
  }
}

function callGetAllImages() {
  if (window.SearchPage && window.SearchPage.callGetAllImages) {
    window.SearchPage.callGetAllImages();
  }
}

function callSearchEmbedding(page = 1) {
  if (window.SearchPage && window.SearchPage.callSearchEmbedding) {
    window.SearchPage.callSearchEmbedding(page);
  }
}

// Reset page functions
function callResetDatabase() {
  if (window.ResetSystemPage && window.ResetSystemPage.callResetDatabase) {
    window.ResetSystemPage.callResetDatabase();
  }
}

function callGetSystemStatus() {
  if (window.ResetSystemPage && window.ResetSystemPage.callGetSystemStatus) {
    window.ResetSystemPage.callGetSystemStatus();
  }
}

// Export to global scope for legacy compatibility
window.MainApp = {
  showPage,
  logout,
  updatePageVisibility,
  setupFileInputListeners,
  setupFormValidation
};

// =================================================================
// PAGINATION NAVIGATION FUNCTIONS
// =================================================================

/**
 * Navigate to previous page for people list
 */
function navigatePreviousPage() {
  console.log('⬅️ navigatePreviousPage called');
  
  if (!window.nguoiSearchState) {
    console.warn('nguoiSearchState not found');
    return;
  }
  
  const currentPage = window.nguoiSearchState.currentPage;
  console.log(`⬅️ Current page: ${currentPage}`);
  
  if (currentPage > 1) {
    const newPage = currentPage - 1;
    console.log(`⬅️ Navigating to page: ${newPage}`);
    
    // Call appropriate search function based on current query
    if (window.nguoiSearchState.currentQuery) {
      console.log(`⬅️ Calling callSearchNguoi(${newPage}) with query`);
      callSearchNguoi(newPage);
    } else {
      console.log(`⬅️ Calling callGetAllNguoi(${newPage}) without query`);
      const sortSelect = document.getElementById('sortNguoiSelect');
      const sortBy = sortSelect ? sortSelect.value : 'ten_asc';
      callGetAllNguoi(newPage, sortBy);
    }
  } else {
    console.log('⬅️ Already at first page');
    // Already at first page
    if (window.showSnackbar) {
      window.showSnackbar('Đã ở trang đầu tiên', 'warning');
    }
  }
}

/**
 * Navigate to next page for people list
 */
function navigateNextPage() {
  console.log('➡️ navigateNextPage called');
  
  if (!window.nguoiSearchState) {
    console.warn('nguoiSearchState not found');
    return;
  }
  
  const currentPage = window.nguoiSearchState.currentPage;
  const totalPages = window.nguoiSearchState.totalPages;
  
  console.log(`📊 Current: ${currentPage}, Total: ${totalPages}`);
  
  if (currentPage < totalPages) {
    const newPage = currentPage + 1;
    console.log(`➡️ Navigating to page: ${newPage}`);
    
    // Call appropriate search function based on current query
    if (window.nguoiSearchState.currentQuery) {
      console.log(`➡️ Calling callSearchNguoi(${newPage}) with query`);
      callSearchNguoi(newPage);
    } else {
      console.log(`➡️ Calling callGetAllNguoi(${newPage}) without query`);
      const sortSelect = document.getElementById('sortNguoiSelect');
      const sortBy = sortSelect ? sortSelect.value : 'ten_asc';
      callGetAllNguoi(newPage, sortBy);
    }
  } else {
    console.log('➡️ Already at last page');
    // Already at last page
    if (window.showSnackbar) {
      window.showSnackbar('Đã ở trang cuối cùng', 'warning');
    }
  }
}

/**
 * Navigate to previous page for embedding search
 */
function navigateEmbeddingPreviousPage() {
  console.log('⬅️ navigateEmbeddingPreviousPage called');
  
  if (!window.embeddingSearchState) {
    console.warn('embeddingSearchState not found');
    return;
  }
  
  const currentPage = window.embeddingSearchState.currentPage;
  console.log(`⬅️ Current page: ${currentPage}`);
  
  if (currentPage > 1) {
    const newPage = currentPage - 1;
    console.log(`⬅️ Calling callSearchEmbedding with page: ${newPage}`);
    callSearchEmbedding(newPage);
  } else {
    console.log('⬅️ Already at first page');
    if (window.showSnackbar) {
      window.showSnackbar('Đã ở trang đầu tiên', 'warning');
    }
  }
}

/**
 * Navigate to next page for embedding search
 */
function navigateEmbeddingNextPage() {
  console.log('🔄 navigateEmbeddingNextPage called');
  
  if (!window.embeddingSearchState) {
    console.warn('embeddingSearchState not found');
    return;
  }
  
  const currentPage = window.embeddingSearchState.currentPage;
  const totalPages = window.embeddingSearchState.totalPages;
  
  console.log(`📊 Current: ${currentPage}, Total: ${totalPages}`);
  
  if (currentPage < totalPages) {
    const newPage = currentPage + 1;
    console.log(`➡️ Calling callSearchEmbedding with page: ${newPage}`);
    callSearchEmbedding(newPage);
  } else {
    console.log('➡️ Already at last page');
    if (window.showSnackbar) {
      window.showSnackbar('Đã ở trang cuối cùng', 'warning');
    }
  }
}

/**
 * Update page indicator text
 */
function updatePageIndicator(type, currentPage, totalPages) {
  const indicatorId = type === 'nguoi' ? 'nguoiPageIndicator' : 'embeddingPageIndicator';
  const indicator = document.getElementById(indicatorId);
  
  if (indicator) {
    indicator.textContent = `Trang ${currentPage} / ${totalPages}`;
  }
  
  // Update navigation button states
  updateNavigationButtons(type, currentPage, totalPages);
}

/**
 * Update navigation button states (enable/disable)
 */
function updateNavigationButtons(type, currentPage, totalPages) {
  const prefix = type === 'nguoi' ? 'nguoi' : 'embedding';
  const prevBtn = document.getElementById(`${prefix}PrevBtn`);
  const nextBtn = document.getElementById(`${prefix}NextBtn`);
  
  if (prevBtn) {
    if (currentPage <= 1) {
      prevBtn.disabled = true;
      prevBtn.classList.add('opacity-50', 'cursor-not-allowed');
    } else {
      prevBtn.disabled = false;
      prevBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    }
  }
  
  if (nextBtn) {
    if (currentPage >= totalPages) {
      nextBtn.disabled = true;
      nextBtn.classList.add('opacity-50', 'cursor-not-allowed');
    } else {
      nextBtn.disabled = false;
      nextBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    }
  }
}

/**
 * Jump to specific page
 */
function goToPage(type, pageNumber) {
  const state = type === 'nguoi' ? window.nguoiSearchState : window.embeddingSearchState;
  
  if (!state) return;
  
  const page = parseInt(pageNumber);
  if (page >= 1 && page <= state.totalPages) {
    if (type === 'nguoi') {
      if (state.currentQuery) {
        callSearchNguoi(page);
      } else {
        const sortSelect = document.getElementById('sortNguoiSelect');
        const sortBy = sortSelect ? sortSelect.value : 'ten_asc';
        callGetAllNguoi(page, sortBy);
      }
    } else {
      callSearchEmbedding(page);
    }
    
    updatePageIndicator(type, page, state.totalPages);
    
    if (window.showSnackbar) {
      window.showSnackbar(`Đã chuyển đến trang ${page}`, 'success');
    }
  }
}

// Make functions globally available
window.navigatePreviousPage = navigatePreviousPage;
window.navigateNextPage = navigateNextPage;
window.navigateEmbeddingPreviousPage = navigateEmbeddingPreviousPage;
window.navigateEmbeddingNextPage = navigateEmbeddingNextPage;
window.updatePageIndicator = updatePageIndicator;
window.updateNavigationButtons = updateNavigationButtons;
window.goToPage = goToPage;
