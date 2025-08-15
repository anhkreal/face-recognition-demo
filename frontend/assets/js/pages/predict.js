/**
 * Predict Page Module
 * Handles face prediction/verification functionality
 */

function callPredict() {
  const file = document.getElementById('predictFile').files[0];
  const resultId = 'predictResult';
  if (!file) {
    window.UIUtils.showApiResult(resultId, { error: 'Vui lòng chọn một file ảnh.' });
    return;
  }
  
  // Show snackbar for starting process
  if (window.showSnackbar) {
    window.showSnackbar('Đang phân tích khuôn mặt...', 'info');
  }
  
  const formData = new FormData();
  formData.append('image', file);
  
  // Show global loading for predict operations
  if (window.showGlobalLoading) {
    window.showGlobalLoading();
  } else {
    window.UIUtils.showLoading(resultId, true);
  }
  
  fetch(`${window.API_CONFIG.host}/predict`, { 
    method: 'POST', 
    body: formData
  })
    .then(res => res.json())
    .then(data => {
        if (window.hideGlobalLoading) {
          window.hideGlobalLoading();
        }
        
        const resultEl = document.getElementById(resultId);
        
        // Check for error field instead of success field
        if (data.error) {
            window.UIUtils.showEmptyState(resultId, 
              'Không thể phân tích', 
              data.error || 'Có lỗi xảy ra khi phân tích khuôn mặt.',
              'fa-exclamation-triangle'
            );
            return;
        }
        
        // Check if we have valid prediction data
        if (!data.pred_age && data.pred_age !== 0 || !data.pred_gender) {
            window.UIUtils.showEmptyState(resultId, 
              'Không thể phân tích', 
              'Không thể nhận diện tuổi và giới tính trong ảnh.',
              'fa-exclamation-triangle'
            );
            return;
        }
        
        let html = `
          <div class="bg-white border border-gray-200 rounded-lg shadow-sm p-4 transition-all duration-300 hover:shadow-xl hover:border-blue-300">
            <div class="font-semibold text-blue-700 flex items-center gap-2 mb-3">
              <i class="fa-solid fa-user-check"></i>
              Kết quả dự đoán
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="bg-blue-50 rounded-lg p-4">
                <div class="flex items-center gap-2 mb-2">
                  <i class="fa-solid fa-birthday-cake text-blue-600"></i>
                  <span class="font-semibold text-blue-800">Tuổi dự đoán</span>
                </div>
                <div class="text-2xl font-bold text-blue-600">${data.pred_age} tuổi</div>
              </div>
              <div class="bg-pink-50 rounded-lg p-4">
                <div class="flex items-center gap-2 mb-2">
                  <i class="fa-solid fa-venus-mars text-pink-600"></i>
                  <span class="font-semibold text-pink-800">Giới tính</span>
                </div>
                <div class="text-xl font-bold text-pink-600">${data.pred_gender === 'Male' ? 'Nam' : 'Nữ'}</div>
              </div>
            </div>
          </div>`;
        resultEl.innerHTML = html;
        
        // Show success snackbar
        if (window.showSnackbar) {
          window.showSnackbar(`Dự đoán thành công: ${data.pred_gender === 'Male' ? 'Nam' : 'Nữ'}, ${data.pred_age} tuổi`, 'success');
        }
    })
    .catch(err => {
        if (window.hideGlobalLoading) {
          window.hideGlobalLoading();
        }
        console.error('Error calling predict API:', err);
        window.UIUtils.showApiResult(resultId, { error: err.message || 'Lỗi kết nối đến server. Vui lòng thử lại sau.' });
        
        // Show error snackbar
        if (window.showSnackbar) {
          window.showSnackbar('Có lỗi xảy ra khi phân tích khuôn mặt', 'error');
        }
    });
}

// Export to global scope
window.PredictPage = {
  callPredict
};
