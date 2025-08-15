/**
 * Query Page Module
 * Handles face recognition functionality
 */

function callQuery() {
  const file = document.getElementById('queryFile').files[0];
  const resultId = 'queryResult';
  if (!file) {
    window.UIUtils.showApiResult(resultId, { error: 'Vui lòng chọn một file ảnh.' });
    return;
  }
  
  // Show snackbar for starting process
  if (window.showSnackbar) {
    window.showSnackbar('Đang nhận diện khuôn mặt...', 'info');
  }
  
  const formData = new FormData();
  formData.append('image', file);
  
  // Show global loading for query operations
  if (window.showGlobalLoading) {
    window.showGlobalLoading();
  } else {
    window.UIUtils.showLoading(resultId, true);
  }
  
  fetch(`${window.API_CONFIG.host}/query`, { 
    method: 'POST', 
    body: formData
  })
    .then(res => res.json())
    .then(data => {
        if (window.hideGlobalLoading) {
          window.hideGlobalLoading();
        }
        
        const resultEl = document.getElementById(resultId);
        if (!data || (Array.isArray(data.results) && data.results.length === 0)) {
            window.UIUtils.showEmptyState(resultId, 
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
        window.UIUtils.showApiResult(resultId, { error: err.message || String(err) });
    });
}

// Export to global scope
window.QueryPage = {
  callQuery
};
