/**
 * Validation Module
 * Handles form validation logic
 */

function validateImageId(fieldId) {
  const field = document.getElementById(fieldId);
  const validation = document.getElementById(fieldId + '-validation');
  const value = field.value.trim();
  if (!value) {
    clearValidation(field, validation);
    return true;
  }
  // Không kiểm tra pattern hay số lượng ký tự cho image_id
  showValidationSuccess(field, validation, 'Hợp lệ');
  return true;
}

function validateClassId(fieldId) {
  const field = document.getElementById(fieldId);
  const validation = document.getElementById(fieldId + '-validation');
  const value = field.value.trim();
  if (!value) {
    clearValidation(field, validation);
    return true;
  }
  // Không kiểm tra pattern hay số lượng ký tự cho class_id
  showValidationSuccess(field, validation, 'Hợp lệ');
  return true;
}

function validateName(fieldId) {
  const field = document.getElementById(fieldId);
  const validation = document.getElementById(fieldId + '-validation');
  const value = field.value.trim();
  
  if (!value) {
    clearValidation(field, validation);
    return true;
  }
  
  if (value.length < 2) {
    showValidationError(field, validation, 'Tên quá ngắn');
    return false;
  } else if (value.length > 50) {
    showValidationError(field, validation, 'Tên quá dài (tối đa 50 ký tự)');
    return false;
  } else if (!/^[a-zA-ZÀ-ỹ\s]+$/.test(value)) {
    showValidationError(field, validation, 'Chỉ được chứa chữ cái và khoảng trắng');
    return false;
  } else {
    showValidationSuccess(field, validation, 'Hợp lệ');
    return true;
  }
}

function validateAge(fieldIdOrValue) {
  // If it's a string that looks like a number, treat it as a value
  if (typeof fieldIdOrValue === 'string' && !isNaN(fieldIdOrValue)) {
    const value = parseInt(fieldIdOrValue);
    return !isNaN(value) && value >= 1 && value <= 120;
  }
  
  // Otherwise, treat it as a field ID (original behavior)
  const field = document.getElementById(fieldIdOrValue);
  if (!field) {
    console.warn('[VALIDATION] Field not found:', fieldIdOrValue);
    return false;
  }
  
  const validation = document.getElementById(fieldIdOrValue + '-validation');
  const value = parseInt(field.value);
  
  if (!field.value) {
    clearValidation(field, validation);
    return true;
  }
  
  if (isNaN(value) || value < 1 || value > 120) {
    if (validation) {
      showValidationError(field, validation, 'Tuổi phải từ 1 đến 120');
    }
    return false;
  } else {
    if (validation) {
      showValidationSuccess(field, validation, 'Hợp lệ');
    }
    return true;
  }
}

function validateLocation(fieldId) {
  const field = document.getElementById(fieldId);
  const validation = document.getElementById(fieldId + '-validation');
  const value = field.value.trim();
  
  if (!value) {
    clearValidation(field, validation);
    return true;
  }
  
  if (value.length < 2) {
    showValidationError(field, validation, 'Địa chỉ quá ngắn');
    return false;
  } else if (value.length > 100) {
    showValidationError(field, validation, 'Địa chỉ quá dài (tối đa 100 ký tự)');
    return false;
  } else {
    showValidationSuccess(field, validation, 'Hợp lệ');
    return true;
  }
}

function validatePath(fieldId) {
  const field = document.getElementById(fieldId);
  const validation = document.getElementById(fieldId + '-validation');
  const value = field.value.trim();
  
  if (!value) {
    clearValidation(field, validation);
    return true;
  }
  
  if (!/\.(jpg|jpeg|png|gif|bmp|webp)$/i.test(value)) {
    showValidationError(field, validation, 'Phải là file ảnh (.jpg, .png, .gif, .webp, v.v.)');
    return false;
  } else {
    showValidationSuccess(field, validation, 'Hợp lệ');
    return true;
  }
}

// Generic ID validation function
function validateId(value) {
  // Basic validation: not empty and reasonable format
  if (!value || typeof value !== 'string') {
    return false;
  }
  const trimmed = value.trim();
  return trimmed.length > 0 && trimmed.length <= 50;
}

function showValidationError(field, validation, message) {
  field.classList.add('input-error');
  field.classList.remove('input-success');
  validation.textContent = message;
  validation.className = 'validation-message validation-error';
}

function showValidationSuccess(field, validation, message) {
  field.classList.add('input-success');
  field.classList.remove('input-error');
  validation.textContent = message;
  validation.className = 'validation-message validation-success';
}

function clearValidation(field, validation) {
  field.classList.remove('input-error', 'input-success');
  validation.textContent = '';
  validation.className = 'validation-message';
}

// Export to global scope
window.Validation = {
  validateImageId,
  validateClassId,
  validateName,
  validateAge,
  validateLocation,
  validatePath,
  validateId,
  showValidationError,
  showValidationSuccess,
  clearValidation
};
