function uploadImage() {
  const fileInput = document.getElementById('fileInput');
  if (!fileInput.files[0]) {
    alert('Chọn ảnh trước!');
    return;
  }
  const formData = new FormData();
  formData.append('file', fileInput.files[0]);
  fetch('http://127.0.0.1:8000/query', {
    method: 'POST',
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById('result').innerHTML =
      `<pre>${JSON.stringify(data, null, 2)}</pre>`;
  })
  .catch(err => {
    document.getElementById('result').innerText = 'Lỗi: ' + err;
  });
}
