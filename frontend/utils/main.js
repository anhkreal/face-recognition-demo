// API Host Configuration
// =================================================================
let apiHost = '';
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
  apiHost = window.location.origin;
} else {
  apiHost = 'http://127.0.0.1:8000';
}

// =================================================================
// Utility Functions
// =================================================================

/**
 * Displays a loading indicator in a specified element.
 * @param {string} resultId - The ID of the element to display the loading indicator in.
 * @param {boolean} show - Whether to show or hide the loading indicator.
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
 * @param {string} resultId - The ID of the element to display empty state in.
 * @param {string} title - Title for empty state
 * @param {string} description - Description for empty state
 * @param {string} icon - Font Awesome icon class
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
 * @param {string} resultId - The ID of the element to display the result in.
 * @param {object} data - The data returned from the API.
 * @param {string} successMessage - The message to display on success.
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
 * A generic function to call an API endpoint.
 * @param {string} endpoint - The API endpoint to call.
 * @param {object} options - The options for the fetch call.
 * @param {string} resultId - The ID of the element to display the result in.
 * @param {string} successMessage - The message to display on success.
 * @param {boolean} useGlobalLoading - Whether to show global loading overlay.
 */
function callApi(endpoint, options, resultId, successMessage, useGlobalLoading = false) {
  if (useGlobalLoading && window.showGlobalLoading) {
    window.showGlobalLoading();
  } else {
    showLoading(resultId, true);
  }
  
  fetch(`${apiHost}/${endpoint}`, options)
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
      showApiResult(resultId, data, successMessage);
    })
    .catch(err => {
      if (useGlobalLoading && window.hideGlobalLoading) {
        window.hideGlobalLoading();
      }
      showApiResult(resultId, { error: err.message || String(err) });
    });
}

// =================================================================
// Page-specific Functions
// =================================================================

function callQuery() {
  const file = document.getElementById('queryFile').files[0];
  const resultId = 'queryResult';
  if (!file) {
    showApiResult(resultId, { error: 'Vui lòng chọn một file ảnh.' });
    return;
  }
  
  // Show snackbar for starting process
  if (window.showSnackbar) {
    window.showSnackbar('Đang nhận diện khuôn mặt...', 'info');
  }
  
  const formData = new FormData();
  formData.append('file', file);
  
  // Show global loading for query operations
  if (window.showGlobalLoading) {
    window.showGlobalLoading();
  } else {
    showLoading(resultId, true);
  }
  
  fetch(`${apiHost}/query`, { method: 'POST', body: formData })
    .then(res => res.json())
    .then(data => {
        if (window.hideGlobalLoading) {
          window.hideGlobalLoading();
        }
        
        const resultEl = document.getElementById(resultId);
        if (!data || (Array.isArray(data.results) && data.results.length === 0)) {
            showEmptyState(resultId, 
              'Không tìm thấy khuôn mặt', 
              'Không thể nhận diện khuôn mặt trong ảnh này. Hãy thử với ảnh khác có khuôn mặt rõ ràng hơn.',
              'fa-user-slash'
            );
            return;
        }
        let results = data.results || [data];
    let html = results.map(item => `
      <div class="bg-white border border-gray-200 rounded-lg shadow-sm p-4 mb-4 transition-all duration-300 hover:shadow-xl hover:border-indigo-300 cursor-pointer">
        <div class="font-semibold text-indigo-700 flex items-center gap-2">
          <i class="fa-solid fa-id-card"></i>
          ID: ${item.image_id}
        </div>
        <div class="text-sm text-gray-600 flex items-center gap-2">
          <i class="fa-solid fa-folder"></i>
          Đường dẫn: <span class="font-mono bg-gray-100 px-2 py-1 rounded">${item.image_path}</span>
        </div>
        <div class="text-sm text-gray-600 flex items-center gap-2">
          <i class="fa-solid fa-tag"></i>
          Class: <span class="font-mono bg-gray-100 px-2 py-1 rounded">${item.class_id}</span>
        </div>
        <div class="text-sm text-gray-600 flex items-center gap-2">
          <i class="fa-solid fa-percentage"></i>
          Score: <span class="font-mono text-green-600 font-bold bg-green-100 px-2 py-1 rounded">${(item.score*100).toFixed(2)}%</span>
        </div>
        ${item.nguoi ? `
          <div class="mt-3 pt-3 border-t border-gray-200">
            <div class="font-bold text-gray-800 flex items-center gap-2 mb-2">
              <i class="fa-solid fa-user"></i>
              Thông tin người:
            </div>
            <div class="grid grid-cols-2 gap-2 text-sm text-gray-700">
              <div class="flex items-center gap-2">
                <i class="fa-solid fa-signature text-blue-500"></i>
                Tên: <span class="font-semibold">${item.nguoi.ten}</span>
              </div>
              <div class="flex items-center gap-2">
                <i class="fa-solid fa-calendar text-green-500"></i>
                Tuổi: <span class="font-semibold">${item.nguoi.tuoi}</span>
              </div>
              <div class="flex items-center gap-2">
                <i class="fa-solid fa-venus-mars text-purple-500"></i>
                Giới tính: <span class="font-semibold">${item.nguoi.gioitinh}</span>
              </div>
              <div class="flex items-center gap-2">
                <i class="fa-solid fa-map-marker-alt text-red-500"></i>
                Nơi ở: <span class="font-semibold">${item.nguoi.noio}</span>
              </div>
            </div>
          </div>
        ` : `<div class="mt-2 text-xs text-gray-400 italic flex items-center gap-2">
          <i class="fa-solid fa-user-slash"></i>
          Không có thông tin người.
        </div>`}
      </div>`).join('');
        resultEl.innerHTML = html;
    })
    .catch(err => {
        if (window.hideGlobalLoading) {
          window.hideGlobalLoading();
        }
        showApiResult(resultId, { error: err.message || String(err) });
    });
}

function callAdd() {
  // Show snackbar for starting process
  if (window.showSnackbar) {
    window.showSnackbar('Đang thêm người mới...', 'info');
  }
  
  const formData = new FormData();
  const file = document.getElementById('addFile').files[0];
  if (file) formData.append('file', file);
  formData.append('image_id', document.getElementById('addImageId').value);
  formData.append('image_path', document.getElementById('addImagePath').value);
  formData.append('class_id', document.getElementById('addClassId').value);
  formData.append('ten', document.getElementById('addTen').value);
  const gioitinh = document.querySelector('input[name="addGioitinh"]:checked')?.value;
  formData.append('gioitinh', gioitinh);
  formData.append('tuoi', document.getElementById('addTuoi').value);
  formData.append('noio', document.getElementById('addNoio').value);
  callApi('add_embedding', { method: 'POST', body: formData }, 'addResult', 'Thêm mới thành công!', true);
  document.getElementById('addForm').reset();
  updateFileName('addFile', 'addFileName', 'Chọn ảnh khuôn mặt (tùy chọn)');
}

function callEdit() {
  const imageId = document.getElementById('editImageId').value;
  if (!imageId) {
      showApiResult('editResult', { error: 'Vui lòng nhập Image ID cần sửa.' });
      return;
  }
  
  // Show snackbar for starting process
  if (window.showSnackbar) {
    window.showSnackbar('Đang cập nhật thông tin...', 'info');
  }
  
  const formData = new FormData();
  const file = document.getElementById('editFile').files[0];
  if (file) formData.append('file', file);
  formData.append('image_id', imageId);
  formData.append('image_path', document.getElementById('editImagePath').value);
  callApi('edit_embedding', { method: 'POST', body: formData }, 'editResult', 'Sửa thành công!', true);
  document.getElementById('editForm').reset();
  updateFileName('editFile', 'editFileName', 'Chọn ảnh mới (tùy chọn)');
}

function callDelete() {
  const deleteType = document.querySelector('input[name="deleteType"]:checked').value;
  const formData = new FormData();
  let endpoint, id;

  if (deleteType === 'embedding') {
    id = document.getElementById('deleteImageId').value;
    if (!id) {
      showApiResult('deleteResult', { error: 'Vui lòng nhập Image ID cần xóa.' });
      return;
    }
    formData.append('image_id', id);
    endpoint = 'delete_image';
  } else {
    id = document.getElementById('deleteClassId').value;
    if (!id) {
      showApiResult('deleteResult', { error: 'Vui lòng nhập Class ID cần xóa.' });
      return;
    }
    formData.append('class_id', id);
    endpoint = 'delete_class';
  }
  callApi(endpoint, { method: 'POST', body: formData }, 'deleteResult', 'Xóa thành công!', true);
  document.getElementById('deleteForm').reset();
}

function callReset() {
  callApi('reset_index', { method: 'POST' }, 'resetResult', 'Reset index thành công!', true);
}

function callSearchNguoi() {
  // Show snackbar for starting process
  if (window.showSnackbar) {
    window.showSnackbar('Đang tìm kiếm người...', 'info');
  }
  
  const query = document.getElementById('searchNguoiInput').value;
  const resultId = 'searchNguoiResult';
  // Lưu trạng thái trang hiện tại vào window
  if (typeof window.nguoiCurrentPage === 'undefined') window.nguoiCurrentPage = 1;
  if (typeof window.nguoiPageSize === 'undefined') window.nguoiPageSize = 15;
  const pageSize = window.nguoiPageSize;
  let currentPage = window.nguoiCurrentPage;
  showLoading(resultId, true);
  // Gọi API với page và page_size
  fetch(`${apiHost}/list_nguoi?query=${encodeURIComponent(query)}&page=${currentPage}&page_size=${pageSize}`)
    .then(res => res.json())
    .then(data => {
      console.log('API /list_nguoi response:', data); // Debug log
      const resultEl = document.getElementById(resultId);
      if (!resultEl) {
        console.error('Element with id', resultId, 'not found!');
        return;
      }
      let results = [];
      let total = 0;
      if (data.results && Array.isArray(data.results.nguoi_list)) {
        results = data.results.nguoi_list;
        total = data.results.total || results.length;
      }
      const totalPages = Math.ceil(total / pageSize);
      // Nếu trang hiện tại vượt quá tổng số trang thì về trang cuối
      if (currentPage > totalPages) currentPage = totalPages;
      if (currentPage < 1) currentPage = 1;
      window.nguoiCurrentPage = currentPage;

      if (data.error) {
        resultEl.innerHTML = `<div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-lg">${data.error}</div>`;
      } else if (!results || results.length === 0) {
        showEmptyState(resultId, 
          'Không tìm thấy người nào', 
          'Không có người nào phù hợp với từ khóa tìm kiếm. Hãy thử tìm kiếm với từ khóa khác hoặc để trống để xem tất cả.',
          'fa-user-slash'
        );
      } else {
        const html = `
          <div class="overflow-x-auto w-full">
            <table class="min-w-full w-full bg-white border rounded-lg shadow-sm">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">STT</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tên</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tuổi</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Giới tính</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nơi ở</th>
                  <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Hành động</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                ${results.map((n, i) => `
                  <tr class="hover:bg-gray-50 transition">
                    <td class="px-4 py-3 text-sm text-gray-700">${(currentPage - 1) * pageSize + i + 1}</td>
                    <td class="px-4 py-3 text-sm font-semibold text-gray-800">${n.ten || n.name || ''}</td>
                    <td class="px-4 py-3 text-sm text-gray-700">${n.tuoi || n.age || ''}</td>
                    <td class="px-4 py-3 text-sm text-gray-700">${n.gioitinh || n.gender || ''}</td>
                    <td class="px-4 py-3 text-sm text-gray-700">${n.noio || n.address || ''}</td>
                    <td class="px-4 py-3 text-center">
                      <button class="bg-red-100 hover:bg-red-200 text-red-700 px-3 py-1 rounded-md transition font-semibold text-xs" onclick="deleteNguoiRow('${n.class_id || n.id || ''}')">Xóa</button>
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
          <div class="mt-4 text-center text-sm text-gray-600">Tổng số: <span class="font-bold">${total}</span> kết quả.</div>
          <div class="flex justify-center items-center gap-2 mt-2">
            <button class="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300" ${currentPage === 1 ? 'disabled' : ''} onclick="window.nguoiCurrentPage--; window.callSearchNguoi()">&lt; Trước</button>
            <span>Trang <input type="number" min="1" max="${totalPages}" value="${currentPage}" style="width: 60px; text-align: center; font-weight: bold; border: 1px solid #e5e7eb; border-radius: 6px; padding: 2px;" onblur="window.handleNguoiPageChange(this.value, ${totalPages})" /> / <span class="font-bold">${totalPages}</span></span>
            <button class="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300" ${currentPage === totalPages ? 'disabled' : ''} onclick="window.nguoiCurrentPage++; window.callSearchNguoi()">Sau &gt;</button>
          </div>
        `;
        resultEl.innerHTML = html;
      }
    })
    .catch(err => {
      console.error('API /list_nguoi error:', err);
      showApiResult(resultId, { error: err.message || String(err) });
    });
}

// Hàm xử lý thay đổi trang người
window.handleNguoiPageChange = function(val, maxPage) {
  let page = parseInt(val);
  if (isNaN(page) || page < 1) page = 1;
  if (page > maxPage) page = maxPage;
  window.nguoiCurrentPage = page;
  window.callSearchNguoi();
};

function deleteNguoiRow(classId) {
    if (!classId || !confirm('Bạn có chắc chắn muốn xóa class này?')) return;
    const formData = new FormData();
    formData.append('class_id', classId);
    
    const resultId = 'searchNguoiResult';
    showLoading(resultId, true);

    fetch(`${apiHost}/delete_class`, { method: 'POST', body: formData })
        .then(res => res.json())
        .then(data => {
            if (data && !data.error) {
                callSearchNguoi(); // Refresh the list
            }
            const message = data.error ? `Lỗi: ${data.error}` : 'Xóa thành công!';
            const tempMsgEl = document.createElement('div');
            tempMsgEl.className = `p-4 mb-4 rounded-lg border-l-4 ${data.error ? 'bg-red-100 border-red-500 text-red-700' : 'bg-green-100 border-green-500 text-green-700'}`;
            tempMsgEl.textContent = message;
            document.getElementById(resultId).prepend(tempMsgEl);
            setTimeout(() => tempMsgEl.remove(), 3000);
        })
        .catch(err => showApiResult(resultId, { error: err.message || String(err) }));
}

// =================================================================
// Event Listeners and Initialization
// =================================================================

window.addEventListener('DOMContentLoaded', function () {
  // Activate the first tab by default
  const firstTab = document.querySelector('.tab-btn');
  if (firstTab) {
    showPage('query', firstTab);
  }

  // Drag & drop cho các vùng file input
  function setupDragDrop(dropAreaId, inputId, labelId, highlightClass = 'border-green-500', bgClass = 'bg-green-50', defaultText = 'Kéo và thả hoặc nhấp để chọn ảnh') {
    const dropArea = document.getElementById(dropAreaId);
    const fileInput = document.getElementById(inputId);
    if (!dropArea || !fileInput) return;
    ['dragenter', 'dragover'].forEach(eventName => {
      dropArea.addEventListener(eventName, e => {
        e.preventDefault();
        e.stopPropagation();
        dropArea.classList.add(highlightClass, bgClass);
      });
    });
    ['dragleave', 'drop'].forEach(eventName => {
      dropArea.addEventListener(eventName, e => {
        e.preventDefault();
        e.stopPropagation();
        dropArea.classList.remove(highlightClass, bgClass);
      });
    });
    dropArea.addEventListener('drop', e => {
      const files = e.dataTransfer.files;
      if (files && files.length > 0) {
        fileInput.files = files;
        updateFileName(inputId, labelId, defaultText);
      }
    });
  }

  // Query file (indigo)
  setupDragDrop('queryDropArea', 'queryFile', 'queryFileName', 'border-indigo-500', 'bg-indigo-50');
  // Add file (green)
  setupDragDrop('addDropArea', 'addFile', 'addFileName', 'border-green-500', 'bg-green-50', 'Chọn ảnh (tùy chọn)');
  // Edit file (yellow)
  setupDragDrop('editDropArea', 'editFile', 'editFileName', 'border-yellow-500', 'bg-yellow-50', 'Chọn ảnh mới (tùy chọn)');

  // Đảm bảo nút tìm kiếm embedding luôn về trang 1
  const embeddingBtn = document.querySelector('#searchEmbeddingForm button[type="button"]');
  if (embeddingBtn) {
    embeddingBtn.onclick = function() {
      embeddingCurrentPage = 1;
      callSearchEmbedding();
    };
  }

  // Đảm bảo nút tìm kiếm người luôn về trang 1
  const nguoiBtn = document.querySelector('#searchNguoiForm button[type="button"]');
  if (nguoiBtn) {
    nguoiBtn.onclick = function() {
      window.nguoiCurrentPage = 1;
      callSearchNguoi();
    };
  }
});

// Make functions globally available
window.showPage = (pageId, btn) => {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  if (btn) btn.classList.add('active');
  document.getElementById(pageId).classList.add('active');
  // Nếu chuyển sang tab người thì hiển thị toàn bộ danh sách
  if (pageId === 'nguoi') {
    document.getElementById('searchNguoiInput').value = '';
    callSearchNguoi();
  }
};

window.updateFileName = (inputId, labelId, defaultText = 'Kéo và thả hoặc nhấp để chọn ảnh') => {
  const input = document.getElementById(inputId);
  const label = document.getElementById(labelId);
  if (input.files.length > 0) {
    const file = input.files[0];
    const fileSize = (file.size / 1024 / 1024).toFixed(2); // MB
    label.innerHTML = `
      <span class="block font-medium text-green-700">${file.name}</span>
      <span class="text-sm text-gray-500">Kích thước: ${fileSize} MB</span>
    `;
  } else {
    if (defaultText.includes('(tùy chọn)') || defaultText.includes('mới')) {
      label.innerHTML = `
        <span class="block font-medium">${defaultText}</span>
        <span class="text-sm text-gray-400">Định dạng: JPG, PNG, WEBP. Kích thước tối đa: 10MB</span>
      `;
    } else {
      label.innerHTML = `
        <span class="block font-medium">${defaultText}</span>
        <span class="text-sm text-gray-400">Định dạng: JPG, PNG, WEBP. Kích thước tối đa: 10MB</span>
      `;
    }
  }
};

window.callQuery = callQuery;
window.callAdd = callAdd;
window.callEdit = callEdit;
window.callDelete = callDelete;
window.callReset = callReset;
window.callSearchNguoi = callSearchNguoi;
window.deleteNguoiRow = deleteNguoiRow;
window.callSearchEmbedding = callSearchEmbedding;
window.showEmptyState = showEmptyState;
window.showApiResult = showApiResult;


// =================================================================
// Embedding search logic
let embeddingCurrentPage = 1;
let embeddingPageSize = 15;
function callSearchEmbedding() {
  // Show snackbar for starting process
  if (window.showSnackbar) {
    window.showSnackbar('Đang tìm kiếm embedding...', 'info');
  }
  
  const query = document.getElementById('searchEmbeddingInput').value;
  const resultId = 'searchEmbeddingResult';
  if (typeof embeddingCurrentPage === 'undefined') embeddingCurrentPage = 1;
  if (typeof embeddingPageSize === 'undefined') embeddingPageSize = 15;
  const pageSize = embeddingPageSize;
  let currentPage = embeddingCurrentPage;
  showLoading(resultId, true);
  fetch(`${apiHost}/search_embeddings?query=${query}&page=${currentPage}&page_size=${pageSize}`)
    .then(res => res.json())
    .then(data => {
      const resultEl = document.getElementById(resultId);
      let results = [];
      let total = 0;
      if (data.results && Array.isArray(data.results)) {
        results = data.results;
        total = data.total || results.length;
      }
      const totalPages = Math.ceil(total / pageSize);
      if (currentPage > totalPages) currentPage = totalPages;
      if (currentPage < 1) currentPage = 1;
      embeddingCurrentPage = currentPage;
      if (data.error) {
        resultEl.innerHTML = `<div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-lg">${data.error}</div>`;
      } else if (!results || results.length === 0) {
        showEmptyState('searchEmbeddingResult', 
          'Không tìm thấy embedding', 
          'Không có embedding nào phù hợp với class_id này. Hãy kiểm tra lại hoặc để trống để xem tất cả.',
          'fa-database'
        );
      } else {
        const html = `
          <div class="overflow-x-auto w-full">
            <table class="min-w-full w-full bg-white border rounded-lg shadow-sm">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">STT</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Image ID</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Image Path</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Class ID</th>
                  <th class="px-4 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">Hành động</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                ${results.map((n, i) => `
                  <tr class="hover:bg-gray-50 transition">
                    <td class="px-4 py-3 text-sm text-gray-700">${(currentPage - 1) * pageSize + i + 1}</td>
                    <td class="px-4 py-3 text-sm font-semibold text-gray-800">${n.image_id}</td>
                    <td class="px-4 py-3 text-sm font-mono text-gray-700">${n.image_path}</td>
                    <td class="px-4 py-3 text-sm text-gray-700">${n.class_id}</td>
                    <td class="px-4 py-3 text-center">
                      <button class="bg-red-100 hover:bg-red-200 text-red-700 px-3 py-1 rounded-md transition font-semibold text-xs" onclick="window.deleteEmbeddingRow('${n.image_id}')">Xóa</button>
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
          <div class="mt-4 text-center text-sm text-gray-600">Tổng số: <span class="font-bold">${total}</span> kết quả.</div>
          <div class="flex justify-center items-center gap-2 mt-2">
            <button class="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300" ${currentPage === 1 ? 'disabled' : ''} onclick="embeddingCurrentPage--; window.callSearchEmbedding()">&lt; Trước</button>
            <span>Trang <input type="number" min="1" max="${totalPages}" value="${currentPage}" style="width: 60px; text-align: center; font-weight: bold; border: 1px solid #e5e7eb; border-radius: 6px; padding: 2px;" onblur="window.handleEmbeddingPageChange(this.value, ${totalPages})" /> / <span class="font-bold">${totalPages}</span></span>
            <button class="px-3 py-1 rounded bg-gray-200 hover:bg-gray-300" ${currentPage === totalPages ? 'disabled' : ''} onclick="embeddingCurrentPage++; window.callSearchEmbedding()">Sau &gt;</button>
          </div>
        `;
        resultEl.innerHTML = html;
// Xóa embedding theo image_id
window.deleteEmbeddingRow = function(imageId) {
  if (!imageId || !confirm('Bạn có chắc chắn muốn xóa embedding này?')) return;
  const formData = new FormData();
  formData.append('image_id', imageId);
  const resultId = 'searchEmbeddingResult';
  showLoading(resultId, true);
  fetch(`${apiHost}/delete_image`, { method: 'POST', body: formData })
    .then(res => res.json())
    .then(data => {
      if (data && !data.error) {
        callSearchEmbedding(); // Refresh the list
      }
      const message = data.error ? `Lỗi: ${data.error}` : 'Xóa thành công!';
      const tempMsgEl = document.createElement('div');
      tempMsgEl.className = `p-4 mb-4 rounded-lg border-l-4 ${data.error ? 'bg-red-100 border-red-500 text-red-700' : 'bg-green-100 border-green-500 text-green-700'}`;
      tempMsgEl.textContent = message;
      document.getElementById(resultId).prepend(tempMsgEl);
      setTimeout(() => tempMsgEl.remove(), 3000);
    })
    .catch(err => showApiResult(resultId, { error: err.message || String(err) }));
};
      }
    })
    .catch(err => {
      document.getElementById(resultId).innerHTML = `<div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-lg">${err.message || err}</div>`;
    });
}

// Hàm xử lý thay đổi trang embedding
window.handleEmbeddingPageChange = function(val, maxPage) {
  let page = parseInt(val);
  if (isNaN(page) || page < 1) page = 1;
  if (page > maxPage) page = maxPage;
  embeddingCurrentPage = page;
  window.callSearchEmbedding();
};

window.callSearchEmbedding = callSearchEmbedding;