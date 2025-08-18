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
        
        // Handle different response types based on action only
        if (data.action === "auto_added") {
            // Auto-added case - new person was automatically created
            const html = `
              <div class="bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 rounded-lg shadow-md p-6 mb-4 transition-all duration-300">
                <div class="flex items-center gap-3 mb-4">
                  <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                    <i class="fa-solid fa-user-plus text-2xl text-green-600"></i>
                  </div>
                  <div>
                    <h3 class="font-bold text-green-800 text-lg">Người mới đã được thêm tự động!</h3>
                    <p class="text-green-600 text-sm">${data.message}</p>
                  </div>
                </div>
                
                <div class="bg-white rounded-lg p-4 border border-green-200">
                  <div class="font-semibold text-green-700 flex items-center gap-2 mb-3">
                    <i class="fa-solid fa-id-card"></i>
                    Thông tin người mới:
                  </div>
                  
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                    <div class="flex items-center gap-2">
                      <i class="fa-solid fa-tag text-indigo-500"></i>
                      <span class="text-gray-600">ID:</span>
                      <span class="font-mono bg-indigo-100 px-2 py-1 rounded text-indigo-700 font-bold">${data.image_id}</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <i class="fa-solid fa-layer-group text-purple-500"></i>
                      <span class="text-gray-600">Class:</span>
                      <span class="font-mono bg-purple-100 px-2 py-1 rounded text-purple-700 font-bold">${data.class_id}</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <i class="fa-solid fa-signature text-blue-500"></i>
                      <span class="text-gray-600">Tên:</span>
                      <span class="font-semibold text-blue-700">${data.ten}</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <i class="fa-solid fa-calendar text-green-500"></i>
                      <span class="text-gray-600">Tuổi:</span>
                      <span class="font-semibold text-green-700">${data.tuoi}</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <i class="fa-solid fa-venus-mars text-pink-500"></i>
                      <span class="text-gray-600">Giới tính:</span>
                      <span class="font-semibold text-pink-700">${data.gioitinh}</span>
                    </div>
                    ${data.predict_used ? `
                      <div class="flex items-center gap-2">
                        <i class="fa-solid fa-robot text-orange-500"></i>
                        <span class="text-gray-600">AI Prediction:</span>
                        <span class="bg-orange-100 text-orange-700 px-2 py-1 rounded text-xs font-medium">Đã sử dụng</span>
                      </div>
                    ` : ''}
                  </div>
                </div>
                
                <div class="mt-4 p-3 bg-green-100 rounded-lg">
                  <div class="flex items-center gap-2 text-green-800 text-sm">
                    <i class="fa-solid fa-lightbulb"></i>
                    <span class="font-medium">Lần tới khi upload ảnh tương tự, hệ thống sẽ nhận diện được người này!</span>
                  </div>
                </div>
              </div>
            `;
            resultEl.innerHTML = html;
            
            // Show success snackbar
            if (window.showSnackbar) {
              window.showSnackbar('Đã thêm người mới thành công!', 'success');
            }
            return;
        }
        
        if (data.action === "auto_add_failed") {
            // Auto-add failed case
            const html = `
              <div class="bg-gradient-to-br from-red-50 to-rose-50 border-2 border-red-200 rounded-lg shadow-md p-6 mb-4">
                <div class="flex items-center gap-3 mb-4">
                  <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center">
                    <i class="fa-solid fa-exclamation-triangle text-2xl text-red-600"></i>
                  </div>
                  <div>
                    <h3 class="font-bold text-red-800 text-lg">Không thể nhận diện và thêm mới thất bại</h3>
                    <p class="text-red-600 text-sm">${data.error}</p>
                  </div>
                </div>
                
                <div class="bg-white rounded-lg p-4 border border-red-200">
                  <div class="text-sm text-red-700">
                    <i class="fa-solid fa-info-circle mr-2"></i>
                    <strong>Gợi ý:</strong> Hãy thử với ảnh khác có khuôn mặt rõ ràng hơn hoặc liên hệ admin nếu vấn đề tiếp tục xảy ra.
                  </div>
                </div>
              </div>
            `;
            resultEl.innerHTML = html;
            
            // Show error snackbar
            if (window.showSnackbar) {
              window.showSnackbar('Có lỗi xảy ra khi thêm người mới!', 'error');
            }
            return;
        }
        
        if (!data || (Array.isArray(data.results) && data.results.length === 0)) {
            window.UIUtils.showEmptyState(resultId, 
              'Không tìm thấy khuôn mặt', 
              'Không thể nhận diện khuôn mặt trong ảnh này. Hãy thử với ảnh khác có khuôn mặt rõ ràng hơn.',
              'fa-user-slash'
            );
            return;
        }
        
        // Handle normal recognition results - check if it's face_recognized action  
        if (data.action === "face_recognized") {
            const html = `
              <div class="bg-white border border-gray-200 rounded-lg shadow-sm p-4 mb-4 transition-all duration-300 hover:shadow-xl hover:border-indigo-300 cursor-pointer">
                <div class="flex items-center gap-2 mb-2">
                  <div class="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center">
                    <i class="fa-solid fa-search text-indigo-600"></i>
                  </div>
                  <span class="font-bold text-indigo-700">Đã nhận diện thành công!</span>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm mb-3">
                  <div class="flex items-center gap-2">
                    <i class="fa-solid fa-id-card text-indigo-500"></i>
                    <span class="text-gray-600">ID:</span>
                    <span class="font-mono bg-indigo-100 px-2 py-1 rounded text-indigo-700 font-bold">${data.image_id}</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <i class="fa-solid fa-tag text-purple-500"></i>
                    <span class="text-gray-600">Class:</span>
                    <span class="font-mono bg-purple-100 px-2 py-1 rounded text-purple-700 font-bold">${data.class_id}</span>
                  </div>
                  <div class="flex items-center gap-2 md:col-span-2">
                    <i class="fa-solid fa-percentage text-green-500"></i>
                    <span class="text-gray-600">Độ chính xác:</span>
                    <span class="font-mono text-green-600 font-bold bg-green-100 px-3 py-1 rounded-full">${(data.score*100).toFixed(2)}%</span>
                  </div>
                </div>
                
                ${data.ten ? `
                  <div class="bg-gray-50 rounded-lg p-4 border border-gray-200">
                    <div class="font-bold text-gray-800 flex items-center gap-2 mb-3">
                      <i class="fa-solid fa-user text-blue-500"></i>
                      Thông tin người:
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm text-gray-700">
                      <div class="flex items-center gap-2">
                        <i class="fa-solid fa-signature text-blue-500"></i>
                        <span class="text-gray-600">Tên:</span>
                        <span class="font-semibold text-blue-700">${data.ten}</span>
                      </div>
                      <div class="flex items-center gap-2">
                        <i class="fa-solid fa-calendar text-green-500"></i>
                        <span class="text-gray-600">Tuổi:</span>
                        <span class="font-semibold text-green-700">${data.tuoi}</span>
                      </div>
                      <div class="flex items-center gap-2">
                        <i class="fa-solid fa-venus-mars text-pink-500"></i>
                        <span class="text-gray-600">Giới tính:</span>
                        <span class="font-semibold text-pink-700">${data.gioitinh}</span>
                      </div>
                    </div>
                  </div>
                ` : `
                  <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                    <div class="flex items-center gap-2 text-yellow-800 text-sm">
                      <i class="fa-solid fa-exclamation-triangle"></i>
                      <span class="italic">Không có thông tin chi tiết cho người này.</span>
                    </div>
                  </div>
                `}
              </div>
            `;
            resultEl.innerHTML = html;
            return;
        }
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
