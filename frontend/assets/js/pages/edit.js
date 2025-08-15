/**
 * Edit Embedding Module
 * Handles editing person information in the system
 * Copied from frontend-v3/utils/main.js
 */

function callEdit() {
  const imageId = document.getElementById('editImageId').value;
  if (!imageId) {
      window.UIUtils.showApiResult('editResult', { error: 'Vui lòng nhập Image ID cần sửa.' });
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
  callProtectedApi('edit_embedding', { method: 'POST', body: formData }, 'editResult', 'Sửa thành công!', true);
  document.getElementById('editForm').reset();
  if (window.updateFileName) {
    window.updateFileName('editFile', 'editFileName', 'Chọn ảnh mới (tùy chọn)');
  }
}

// Legacy wrapper function for backward compatibility
function callEditNguoi() {
  callEdit();
}

// Make functions globally available
window.callEdit = callEdit;
window.callEditNguoi = callEditNguoi;