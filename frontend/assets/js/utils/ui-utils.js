/**
 * UI Utilities Module
 * Handles UI components and interactions
 */

/**
 * Displays a loading indicator in a specified element.
 */
function showLoading(resultId, show) {
  const resultEl = document.getElementById(resultId);
  if (!resultEl) return;
  if (show) {
    resultEl.innerHTML = `
      <div class="flex items-center justify-center p-8 bg-gradient-to-r from-indigo-50 to-blue-50 rounded-lg border border-indigo-200">
        <div class="animate-spin rounded-full h-10 w-10 border-b-3 border-indigo-600 mr-4"></div>
        <div>
          <div class="text-gray-700 font-semibold flex items-center gap-2">
            <i class="fa-solid fa-gear fa-spin text-indigo-600"></i>
            Đang xử lý...
          </div>
          <div class="text-sm text-gray-500">Vui lòng chờ trong giây lát</div>
        </div>
      </div>`;
  } else {
    resultEl.innerHTML = '';
  }
}

/**
 * Shows empty state when no data is found
 */
function showEmptyState(resultId, title = 'Không có dữ liệu', description = 'Không tìm thấy kết quả nào.', icon = 'fa-inbox') {
  const resultEl = document.getElementById(resultId);
  if (!resultEl) return;
  
  resultEl.innerHTML = `
    <div class="empty-state">
      <i class="fa-solid ${icon}"></i>
      <h3>${title}</h3>
      <p>${description}</p>
    </div>
  `;
}

/**
 * Displays the result of an API call in a specified element.
 */
function showApiResult(resultId, data, successMessage = 'Thao tác thành công!') {
    const resultEl = document.getElementById(resultId);
    if (!resultEl) return;

    let content;
    if (data.error) {
        // Show error snackbar
        if (window.showSnackbar) {
            window.showSnackbar(data.error, 'error');
        }
        content = `<div class="bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-lg shadow-sm transition-all hover:shadow-md" role="alert">
                     <div class="flex items-center gap-3">
                       <i class="fa-solid fa-exclamation-circle text-red-500 text-xl"></i>
                       <div>
                         <p class="font-bold">Lỗi</p>
                         <p>${data.error}</p>
                       </div>
                     </div>
                   </div>`;
    } else {
        // Show success snackbar
        if (window.showSnackbar) {
            window.showSnackbar(successMessage, 'success');
        }
        content = `<div class="bg-green-50 border-l-4 border-green-500 text-green-700 p-4 rounded-lg shadow-sm transition-all hover:shadow-md" role="alert">
                     <div class="flex items-center gap-3">
                       <i class="fa-solid fa-check-circle text-green-500 text-xl"></i>
                       <div class="flex-1">
                         <p class="font-bold">Thành công</p>
                         <p>${successMessage}</p>
                         <div class="mt-3 bg-gray-800 text-white font-mono rounded-lg p-4 text-sm overflow-auto max-h-60 border border-gray-600">
                           <div class="flex items-center gap-2 mb-2 text-gray-300">
                             <i class="fa-solid fa-code"></i>
                             <span class="text-xs">Response Data:</span>
                           </div>
                           <pre>${JSON.stringify(data, null, 2)}</pre>
                         </div>
                       </div>
                     </div>
                   </div>`;
    }
    resultEl.innerHTML = content;
}

/**
 * Updates file name display - supports both legacy and new calling patterns
 */
// Debug function for UI elements
function debugElementExists(elementId) {
  const element = document.getElementById(elementId);
  console.log(`[DEBUG] Element '${elementId}': ${element ? 'EXISTS' : 'NOT FOUND'}`);
  if (!element) {
    console.log(`[DEBUG] Available elements with similar IDs:`, 
      Array.from(document.querySelectorAll('[id*="' + elementId.substring(0, 5) + '"]'))
        .map(el => el.id).filter(id => id)
    );
  }
  return element;
}

function updateFileName(inputId, param2) {
  console.log(`[DEBUG] updateFileName called with inputId: '${inputId}', param2: '${param2}'`);
  
  // Check if param2 is a string (filename) or element ID
  if (typeof param2 === 'string' && document.getElementById(param2)) {
    // Legacy call: updateFileName(inputId, elementId)
    const input = debugElementExists(inputId);
    const targetElement = debugElementExists(param2);
    
    if (input && targetElement && input.files && input.files.length > 0) {
      const file = input.files[0];
      const fileSize = (file.size / 1024 / 1024).toFixed(2); // MB
      console.log(`[DEBUG] Setting innerHTML for '${param2}' with file: ${file.name}`);
      targetElement.innerHTML = `
        <span class="block font-medium text-green-700">${file.name}</span>
        <span class="text-sm text-gray-500">Kích thước: ${fileSize} MB</span>
      `;
    } else if (targetElement) {
      console.log(`[DEBUG] Setting default innerHTML for '${param2}'`);
      targetElement.innerHTML = `
        <span class="block font-medium">Kéo và thả hoặc nhấp để chọn ảnh</span>
        <span class="text-sm text-gray-400">Định dạng: JPG, PNG, WEBP. Kích thước tối đa: 10MB</span>
      `;
    } else {
      console.error(`[ERROR] Cannot update fileName - input: ${input ? 'found' : 'not found'}, targetElement: ${targetElement ? 'found' : 'not found'}`);
    }
  } else {
    // New call: updateFileName(inputId, fileName)
    const fileName = param2;
    console.log(`[DEBUG] New call format - fileName: '${fileName}'`);
    
    // Try to find file name display element with different possible selectors
    let fileNameEl = document.getElementById(inputId + '-name');
    console.log(`[DEBUG] Trying '${inputId}-name': ${fileNameEl ? 'found' : 'not found'}`);
    
    if (!fileNameEl) {
      fileNameEl = document.querySelector(`[data-file-for="${inputId}"]`);
      console.log(`[DEBUG] Trying '[data-file-for="${inputId}"]': ${fileNameEl ? 'found' : 'not found'}`);
    }
    if (!fileNameEl) {
      fileNameEl = document.querySelector(`#${inputId} + .file-name`);
      console.log(`[DEBUG] Trying '#${inputId} + .file-name': ${fileNameEl ? 'found' : 'not found'}`);
    }
    if (!fileNameEl) {
      fileNameEl = document.querySelector(`label[for="${inputId}"] + .file-name`);
      console.log(`[DEBUG] Trying 'label[for="${inputId}"] + .file-name': ${fileNameEl ? 'found' : 'not found'}`);
    }
    
    if (fileNameEl) {
      if (fileName) {
        console.log(`[DEBUG] Setting textContent for found element: '${fileName}'`);
        fileNameEl.textContent = fileName;
        fileNameEl.style.color = '#16a34a'; // green color for selected file
      } else {
        console.log(`[DEBUG] Clearing textContent for found element`);
        fileNameEl.textContent = '';
      }
    } else {
      console.warn(`[WARNING] No file name element found for inputId: '${inputId}'`);
      // If no file name element found, try to update the label text
      const input = debugElementExists(inputId);
      if (input) {
        const label = input.closest('.file-input-wrapper')?.querySelector('label') || 
                     document.querySelector(`label[for="${inputId}"]`);
        if (label && fileName) {
          const originalText = label.getAttribute('data-original-text') || label.textContent;
          if (!label.getAttribute('data-original-text')) {
            label.setAttribute('data-original-text', originalText);
          }
          label.innerHTML = `<i class="fas fa-check-circle"></i> ${fileName}`;
        } else if (label && !fileName) {
          const originalText = label.getAttribute('data-original-text');
          if (originalText) {
            label.innerHTML = originalText;
          }
        }
      }
    }
  }
}

/**
 * Show page functionality
 */
function showPage(pageId, btn) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  if (btn) btn.classList.add('active');
  document.getElementById(pageId).classList.add('active');
  
  // Nếu chuyển sang tab người thì hiển thị toàn bộ danh sách
  if (pageId === 'searchNguoi') {
    document.getElementById('searchNguoiInput').value = '';
    if (window.SearchPage) {
      window.SearchPage.callSearchNguoi();
    }
  }
}

// Export to global scope
window.UIUtils = {
  showLoading,
  showEmptyState,
  showApiResult,
  updateFileName,
  showPage
};

// Also export updateFileName directly to global scope for legacy HTML compatibility
window.updateFileName = updateFileName;
