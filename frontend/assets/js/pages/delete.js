/**
 * Delete Module
 * Handles deleting person or image from the system
 * Copied from frontend-v3/utils/main.js
 */

function callDelete() {
  const deleteType = document.querySelector('input[name="deleteType"]:checked').value;
  const formData = new FormData();
  let endpoint, id;

  if (deleteType === 'embedding') {
    id = document.getElementById('deleteImageId').value;
    if (!id) {
      window.UIUtils.showApiResult('deleteResult', { error: 'Vui lòng nhập Image ID cần xóa.' });
      return;
    }
    formData.append('image_id', id);
    endpoint = 'delete_image';
  } else {
    id = document.getElementById('deleteClassId').value;
    if (!id) {
      window.UIUtils.showApiResult('deleteResult', { error: 'Vui lòng nhập Class ID cần xóa.' });
      return;
    }
    formData.append('class_id', id);
    endpoint = 'delete_class';
  }
  callProtectedApi(endpoint, { method: 'POST', body: formData }, 'deleteResult', 'Xóa thành công!', true);
  document.getElementById('deleteForm').reset();
}

// Legacy wrapper function for backward compatibility
function callDeleteNguoi() {
  callDelete();
}

// Make functions globally available
window.callDelete = callDelete;
window.callDeleteNguoi = callDeleteNguoi;