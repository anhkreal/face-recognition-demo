/**
 * Add Embedding Module
 * Handles adding new person to the system
 * Copied from frontend-v3/utils/main.js
 */

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
  callProtectedApi('add_embedding', { method: 'POST', body: formData }, 'addResult', 'Thêm mới thành công!', true);
  document.getElementById('addForm').reset();
  if (window.updateFileName) {
    window.updateFileName('addFile', 'addFileName', 'Chọn ảnh khuôn mặt (tùy chọn)');
  }
}

// Legacy wrapper function for backward compatibility
function callAddNguoi() {
  callAdd();
}

// Make functions globally available
window.callAdd = callAdd;
window.callAddNguoi = callAddNguoi;