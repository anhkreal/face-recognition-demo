// Tính độ sắc nét của ảnh bằng phương pháp Laplacian (đánh giá độ mờ)
// Trả về giá trị phương sai của đạo hàm bậc hai (Laplacian) trên ảnh xám
export function varianceOfLaplacian(imageData, width, height) {
      // Chuyển ảnh màu sang ảnh xám
      const gray = new Float32Array(width * height);
      for (let i = 0; i < width * height; i++) {
        const r = imageData.data[i * 4];
        const g = imageData.data[i * 4 + 1];
        const b = imageData.data[i * 4 + 2];
        gray[i] = 0.299 * r + 0.587 * g + 0.114 * b;
      }

      let sum = 0;
      let sumSq = 0;
      let count = 0;

      // Tính toán Laplacian cho từng điểm ảnh (trừ viền)
      for (let y = 1; y < height - 1; y++) {
        for (let x = 1; x < width - 1; x++) {
          const idx = y * width + x;
          // Đạo hàm bậc hai (Laplacian kernel)
          const lap =
            gray[idx - width] +      // pixel trên
            gray[idx + width] +      // pixel dưới
            gray[idx - 1] +          // pixel trái
            gray[idx + 1] -          // pixel phải
            4 * gray[idx];           // pixel trung tâm

          sum += lap;
          sumSq += lap * lap;
          count++;
        }
      }

      if (count === 0) return 0;
      const mean = sum / count;
      return sumSq / count - mean * mean;
    }
// Đánh giá chất lượng khuôn mặt dựa trên keypoints (mắt, mũi, miệng)
// Trả về điểm số càng cao càng tốt (đối xứng, thẳng, cân đối...)
export function calculateFaceQuality(kps) {
      // Kiểm tra keypoint hợp lệ
      for (let kp of kps) {
        if (kp[0] < 0 || kp[1] < 0) {
          return -10;
        }
      }

  // Gán tên cho các điểm đặc trưng
  const [leftEye, rightEye, nose, leftMouth, rightMouth] = kps;
      // Tính trung điểm mắt và miệng
      const eyeCenter = [
        (leftEye[0] + rightEye[0]) / 2,
        (leftEye[1] + rightEye[1]) / 2
      ];
      const mouthCenter = [
        (leftMouth[0] + rightMouth[0]) / 2,
        (leftMouth[1] + rightMouth[1]) / 2
      ];

      // Khoảng cách giữa hai mắt và hai khóe miệng
      const eyeDist = Math.sqrt(
        Math.pow(leftEye[0] - rightEye[0], 2) + 
        Math.pow(leftEye[1] - rightEye[1], 2)
      );
      const mouthDist = Math.sqrt(
        Math.pow(leftMouth[0] - rightMouth[0], 2) + 
        Math.pow(leftMouth[1] - rightMouth[1], 2)
      );

  // Nếu khoảng cách bất thường thì trả về điểm thấp
  if (eyeDist === 0 || mouthDist === 0) return -10;

      // Các chỉ số đánh giá: độ lệch mắt, miệng, vị trí mũi, đối xứng mắt-miệng, tỉ lệ dọc
      const diffEyeY = Math.abs(leftEye[1] - rightEye[1]) / eyeDist; // mắt lệch theo trục Y
      const diffMouthY = Math.abs(leftMouth[1] - rightMouth[1]) / mouthDist; // miệng lệch
      const noseOffset = Math.abs(nose[0] - eyeCenter[0]) / eyeDist; // mũi lệch so với trung tâm mắt
      const mouthOffset = Math.abs(mouthCenter[0] - nose[0]) / mouthDist; // miệng lệch so với mũi
      
      const eyeMouthDist = Math.sqrt(
        Math.pow(mouthCenter[0] - eyeCenter[0], 2) + 
        Math.pow(mouthCenter[1] - eyeCenter[1], 2)
      );
      const verticalRatio = eyeMouthDist > 0 ? (mouthCenter[1] - eyeCenter[1]) / eyeMouthDist : 0; // tỉ lệ dọc

      // Đối xứng mắt - mũi
      const leftEyeToNose = Math.sqrt(
        Math.pow(leftEye[0] - nose[0], 2) + Math.pow(leftEye[1] - nose[1], 2)
      );
      const rightEyeToNose = Math.sqrt(
        Math.pow(rightEye[0] - nose[0], 2) + Math.pow(rightEye[1] - nose[1], 2)
      );
      const diffEyeSymmetry = Math.abs(leftEyeToNose - rightEyeToNose) / eyeDist;

      // Đối xứng miệng - mũi
      const leftMouthToNose = Math.sqrt(
        Math.pow(leftMouth[0] - nose[0], 2) + Math.pow(leftMouth[1] - nose[1], 2)
      );
      const rightMouthToNose = Math.sqrt(
        Math.pow(rightMouth[0] - nose[0], 2) + Math.pow(rightMouth[1] - nose[1], 2)
      );
      const diffMouthSymmetry = Math.abs(leftMouthToNose - rightMouthToNose) / mouthDist;

      // Tính điểm từng tiêu chí (dùng hàm exp để điểm giảm nhanh khi lệch)
      const scoreEyeY = Math.exp(-diffEyeY);
      const scoreMouthY = Math.exp(-diffMouthY);
      const scoreNoseOffset = Math.exp(-noseOffset);
      const scoreMouthOffset = Math.exp(-mouthOffset);
      const scoreVertical = verticalRatio;
      const scoreSymmetryEye = Math.exp(-diffEyeSymmetry);
      const scoreSymmetryMouth = Math.exp(-diffMouthSymmetry);

      // Tổng hợp điểm, trọng số ưu tiên cho các tiêu chí quan trọng
      const totalScore = (
        2 * scoreEyeY +
        1 * scoreMouthY +
        1 * scoreNoseOffset +
        2 * scoreMouthOffset +
        2 * scoreVertical +
        2 * scoreSymmetryEye +
        1 * scoreSymmetryMouth
      );

      return totalScore;
    }
// Căn chỉnh khuôn mặt về vị trí thẳng dựa vào hai mắt, crop vùng khuôn mặt
// Trả về canvas chứa khuôn mặt đã căn chỉnh
export function alignFace(originalCanvas, kps, bbox, padding = 10){
  // Kiểm tra đủ 5 keypoints (2 mắt, mũi, 2 miệng)
  if (kps.length !== 5) {
    debugLog("Invalid keypoint count: " + kps.length);
    return null;
  }

  // Lấy vị trí hai mắt
  const [leftEye, rightEye] = [kps[0], kps[1]];


  // Tính góc nghiêng của khuôn mặt dựa vào hai mắt
  const dy = rightEye[1] - leftEye[1];
  const dx = rightEye[0] - leftEye[0];
  const angleRad = Math.atan2(dy, dx);
  const angleDeg = angleRad * 180.0 / Math.PI;

    const eyeCenterX = (leftEye[0] + rightEye[0]) / 2;
    const eyeCenterY = (leftEye[1] + rightEye[1]) / 2;

    const w = originalCanvas.width;
    const h = originalCanvas.height;

    const angle = -angleRad; // Canvas rotates opposite to OpenCV
    const cosA = Math.cos(angle);
    const sinA = Math.sin(angle);

  // Xác định 4 góc của ảnh gốc
    let corners = [
        [0, 0], [w, 0],
        [0, h], [w, h]
    ];

  // Xoay các góc để tìm bounding box mới sau khi xoay
    let transformed = corners.map(([x, y]) => {
        let tx = (x - eyeCenterX) * cosA - (y - eyeCenterY) * sinA + eyeCenterX;
        let ty = (x - eyeCenterX) * sinA + (y - eyeCenterY) * cosA + eyeCenterY;
        return [tx, ty];
    });

  // Tính kích thước canvas mới sau khi xoay
    let xs = transformed.map(p => p[0]);
    let ys = transformed.map(p => p[1]);
    const minX = Math.min(...xs);
    const maxX = Math.max(...xs);
    const minY = Math.min(...ys);
    const maxY = Math.max(...ys);

    const newW = Math.ceil(maxX - minX);
    const newH = Math.ceil(maxY - minY);

  // Tạo canvas mới để chứa ảnh đã xoay
    const rotatedCanvas = document.createElement('canvas');
    rotatedCanvas.width = newW;
    rotatedCanvas.height = newH;
    const rotCtx = rotatedCanvas.getContext('2d');

  // Dịch chuyển để không bị cắt ảnh khi xoay
    rotCtx.translate(-minX, -minY);
    rotCtx.translate(eyeCenterX, eyeCenterY);
    rotCtx.rotate(-angleRad); // Opposite direction for canvas
    rotCtx.translate(-eyeCenterX, -eyeCenterY);

  // Vẽ ảnh đã xoay lên canvas mới
    rotCtx.drawImage(originalCanvas, 0, 0);

  // Xoay lại bounding box khuôn mặt
    let bboxCorners = [
        [bbox.x1, bbox.y1],
        [bbox.x2, bbox.y1],
        [bbox.x1, bbox.y2],
        [bbox.x2, bbox.y2]
    ];

    let bboxTrans = bboxCorners.map(([x, y]) => {
        let tx = (x - eyeCenterX) * cosA - (y - eyeCenterY) * sinA + eyeCenterX - minX;
        let ty = (x - eyeCenterX) * sinA + (y - eyeCenterY) * cosA + eyeCenterY - minY;
        return [tx, ty];
    });

  // Tính toán lại toạ độ bounding box, thêm padding
    let bx = bboxTrans.map(p => p[0]);
    let by = bboxTrans.map(p => p[1]);
    const minBx = Math.max(0, Math.floor(Math.min(...bx)) - padding);
    const maxBx = Math.min(newW, Math.ceil(Math.max(...bx)) + padding);
    const minBy = Math.max(0, Math.floor(Math.min(...by)) - padding);
    const maxBy = Math.min(newH, Math.ceil(Math.max(...by)) + padding);

  // Kiểm tra kích thước bounding box hợp lệ
    if (maxBx <= minBx || maxBy <= minBy) {
        debugLog("Invalid bounding box dimensions after rotation");
        return null;
    }

  // Cắt vùng khuôn mặt từ canvas đã xoay
    const faceCanvas = document.createElement('canvas');
    faceCanvas.width = maxBx - minBx;
    faceCanvas.height = maxBy - minBy;
    const faceCtx = faceCanvas.getContext('2d');
    faceCtx.drawImage(
        rotatedCanvas,
        minBx, minBy, faceCanvas.width, faceCanvas.height,
        0, 0, faceCanvas.width, faceCanvas.height
    );

  return faceCanvas;
}
// Chuyển đổi giá trị dự đoán (distance) thành toạ độ bounding box
export function distance2bbox(points, distance, maxShape = null) {
      const bboxes = [];
      for (let i = 0; i < points.length; i++) {
        const [px, py] = points[i];
        // Tính toạ độ box dựa vào anchor và distance
        let x1 = px - distance[i * 4];
        let y1 = py - distance[i * 4 + 1];
        let x2 = px + distance[i * 4 + 2];
        let y2 = py + distance[i * 4 + 3];
        
        // Giới hạn trong kích thước ảnh nếu có
        if (maxShape) {
          x1 = Math.max(0, Math.min(x1, maxShape[1]));
          y1 = Math.max(0, Math.min(y1, maxShape[0]));
          x2 = Math.max(0, Math.min(x2, maxShape[1]));
          y2 = Math.max(0, Math.min(y2, maxShape[0]));
        }
        bboxes.push([x1, y1, x2, y2]);
      }
      return bboxes;
    }

// Chuyển đổi giá trị dự đoán thành toạ độ các keypoints (mắt, mũi, miệng...)
export function distance2kps(points, distance, maxShape = null) {
  // Số lượng keypoints trên mỗi khuôn mặt
  const numKps = distance.length / (points.length * 2);
      const kpss = [];
      
      for (let i = 0; i < points.length; i++) {
        const [px, py] = points[i];
        const kps = [];
        // Tính toạ độ từng keypoint
        for (let j = 0; j < numKps; j++) {
          let kx = px + distance[i * numKps * 2 + j * 2];
          let ky = py + distance[i * numKps * 2 + j * 2 + 1];
          
          if (maxShape) {
            kx = Math.max(0, Math.min(kx, maxShape[1]));
            ky = Math.max(0, Math.min(ky, maxShape[0]));
          }
          kps.push([kx, ky]);
        }
        kpss.push(kps);
      }
      return kpss;
    }

// Non-Maximum Suppression: loại bỏ các bounding box trùng lặp, chỉ giữ lại box có điểm cao nhất
export  function nms(dets, thresh = 0.4) {
  if (!dets.length) return [];
      
      // Sắp xếp các box theo điểm số giảm dần
      const sortedDets = dets.map((det, index) => ({ det, index }))
        .sort((a, b) => b.det[4] - a.det[4]);
      
  const keep = [];
  const suppressed = new Set(); // lưu các box đã loại bỏ
      
      for (let i = 0; i < sortedDets.length; i++) {
        const { det: detA, index: idxA } = sortedDets[i];
        if (suppressed.has(idxA)) continue;
        
        keep.push(idxA);
        // So sánh box hiện tại với các box còn lại
        for (let j = i + 1; j < sortedDets.length; j++) {
          const { det: detB, index: idxB } = sortedDets[j];
          if (suppressed.has(idxB)) continue;
          // Tính diện tích giao nhau
          const xx1 = Math.max(detA[0], detB[0]);
          const yy1 = Math.max(detA[1], detB[1]);
          const xx2 = Math.min(detA[2], detB[2]);
          const yy2 = Math.min(detA[3], detB[3]);
          
          const w = Math.max(0, xx2 - xx1 + 1);
          const h = Math.max(0, yy2 - yy1 + 1);
          const inter = w * h;
          
          const areaA = (detA[2] - detA[0] + 1) * (detA[3] - detA[1] + 1);
          const areaB = (detB[2] - detB[0] + 1) * (detB[3] - detB[1] + 1);
          const ovr = inter / (areaA + areaB - inter);
          // Nếu trùng lặp lớn hơn ngưỡng thì loại bỏ box điểm thấp hơn
          if (ovr > thresh) {
            suppressed.add(idxB);
          }
        }
      }
      
      return keep;
    }

// Gửi ảnh khuôn mặt tốt nhất lên server qua HTTP POST
// Dùng cho các ứng dụng nhận diện, lưu trữ, phân tích ở backend
export async function sendBestFaceToServer(faceDataUrl) {
  // Địa chỉ server nhận ảnh (cần thay đổi phù hợp)
  const serverUrl = 'http://127.0.0.1:8000/query';
  
  try {
    debugLog("Preparing to send best face to server...");
    const status = document.getElementById('status');
    status.innerHTML = '<div style="color: #ff9800;">📤 Sending best face to server...</div>';
    
    // Kiểm tra dữ liệu đầu vào
    if (!faceDataUrl) {
      throw new Error('No face data URL provided');
    }
    // Kiểm tra định dạng data URL
    if (!faceDataUrl.startsWith('data:image/')) {
      throw new Error('Invalid data URL format');
    }
    
    debugLog(`Data URL length: ${faceDataUrl.length}`);
    debugLog(`Data URL prefix: ${faceDataUrl.substring(0, 50)}...`);
    
    // Chuyển data URL thành Blob để gửi
    const response = await fetch(faceDataUrl);
    const blob = await response.blob();
    
    debugLog(`Blob size: ${blob.size} bytes, type: ${blob.type}`);
    
    // Kiểm tra kích thước blob
    if (blob.size === 0) {
      throw new Error('Generated blob is empty');
    }
    if (blob.size > 10 * 1024 * 1024) { // 10MB limit
      throw new Error('Image too large (>10MB)');
    }
    
    // Tạo FormData để gửi file và thông tin liên quan
    const formData = new FormData();
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const filename = `best_face_${timestamp}.png`;
    
    formData.append('image', blob, filename);
    formData.append('score', bestScore.toFixed(2));
    formData.append('timestamp', timestamp);
    formData.append('processed_faces', processedFacesCount.toString());
    
    // Debug nội dung gửi đi
    debugLog(`FormData entries:`);
    for (let [key, value] of formData.entries()) {
      if (key === 'image') {
        debugLog(`  ${key}: [File] ${value.name}, size: ${value.size}, type: ${value.type}`);
      } else {
        debugLog(`  ${key}: ${value}`);
      }
    }
    
    debugLog(`Sending ${filename} to ${serverUrl}...`);
    
    // Ping thử server trước khi gửi
    try {
      const pingResponse = await fetch(serverUrl.replace('/predict', '/'), { 
        method: 'GET',
        mode: 'no-cors' // Tránh lỗi CORS khi ping
      });
      debugLog('Server ping successful');
    } catch (pingError) {
      debugLog(`Server ping failed: ${pingError.message}`);
    }
    
    // Gửi POST request với timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000); // timeout 30s
    
    const serverResponse = await fetch(serverUrl, {
      method: 'POST',
      body: formData,
      signal: controller.signal,
      // Không thêm Content-Type header khi dùng FormData
      headers: {
        // 'Accept': 'application/json', // Có thể thêm nếu server yêu cầu
      }
    });
    
    clearTimeout(timeoutId);
    
    // Log phản hồi từ server
    debugLog(`Response status: ${serverResponse.status}`);
    debugLog(`Response statusText: ${serverResponse.statusText}`);
    debugLog(`Response headers:`);
    for (let [key, value] of serverResponse.headers.entries()) {
      debugLog(`  ${key}: ${value}`);
    }
    
    if (serverResponse.ok) {
      const result = await serverResponse.text();
      debugLog("Server response: " + result);
      status.innerHTML = '<div style="color: #4CAF50;">✅ Best face sent successfully to server!</div>';
      return { success: true, response: result };
    } else {
      // Đọc error response từ server
      let errorDetails = '';
      try {
        errorDetails = await serverResponse.text();
        debugLog(`Server error details: ${errorDetails}`);
      } catch (readError) {
        debugLog(`Could not read error response: ${readError.message}`);
      }
      
      throw new Error(`Server responded with status: ${serverResponse.status} ${serverResponse.statusText}. Details: ${errorDetails}`);
    }
    
  } catch (error) {
    console.error('Failed to send best face to server:', error);
    debugLog("Failed to send to server: " + error.message);
    
    let errorMessage = error.message;
    if (error.name === 'AbortError') {
      errorMessage = 'Request timeout (30s)';
    } else if (error.name === 'TypeError' && error.message.includes('fetch')) {
      errorMessage = 'Network error - cannot reach server';
    }
    
    const status = document.getElementById('status');
    status.innerHTML = '<div style="color: red;">❌ Failed to send to server: ' + errorMessage + '</div>';
    return { success: false, error: errorMessage };
  }
}
