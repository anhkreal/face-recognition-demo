/**
 * Search Page Module
 * Handles search functionality for people and images
 */

// Pagination state
let embeddingSearchState = {
  currentPage: 1,
  pageSize: 15,
  totalPages: 0,
  totalResults: 0,
  currentQuery: ''
};

let nguoiSearchState = {
  currentPage: 1,
  pageSize: 15,
  totalPages: 0,
  totalResults: 0,
  currentQuery: ''
};

function callSearchNguoi(page = 1) {
  const searchInput = document.getElementById('searchNguoiInput');
  const resultId = 'searchNguoiResult';
  
  if (!searchInput) {
    window.UIUtils.showApiResult(resultId, { error: 'Input tìm kiếm không tồn tại.' });
    return;
  }
  
  const query = searchInput.value?.trim();
  
  // Update state
  nguoiSearchState.currentQuery = query || '';
  nguoiSearchState.currentPage = page;
  
  // If empty, show all people
  if (!query) {
    callGetAllNguoi(page);
    return;
  }
  
  // Show snackbar for starting process
  if (window.showSnackbar) {
    window.showSnackbar('Đang tìm kiếm...', 'info');
  }
  
  window.UIUtils.showLoading(resultId, true);
  
  // Use list_nguoi API with query parameter and pagination
  const params = new URLSearchParams();
  params.append('query', query);
  params.append('page', page);
  params.append('page_size', nguoiSearchState.pageSize);
  
  fetch(`${window.API_CONFIG.host}/list_nguoi?${params.toString()}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(res => res.json())
    .then(data => {
        console.log('Search nguoi response:', data);  // Debug log
        const resultEl = document.getElementById(resultId);
        
        if (data.error) {
            window.UIUtils.showEmptyState(resultId, 
              'Không thể tìm kiếm', 
              data.error || 'Có lỗi xảy ra khi tìm kiếm.',
              'fa-exclamation-triangle'
            );
            return;
        }
        
        // API returns { results: { nguoi_list: [...], total: number } }
        const apiData = data.results || {};
        const people = apiData.nguoi_list || [];
        
        // Update pagination state
        nguoiSearchState.totalResults = apiData.total || 0;
        nguoiSearchState.totalPages = Math.ceil(nguoiSearchState.totalResults / nguoiSearchState.pageSize);
        
        if (people.length === 0) {
            window.UIUtils.showEmptyState(resultId, 
              'Không tìm thấy kết quả', 
              `Không có người nào phù hợp với từ khóa: "${query}"`,
              'fa-search'
            );
            return;
        }
            
        // Create table HTML
        const tableHtml = `
          <div class="overflow-x-auto">
            <table class="min-w-full bg-white border border-gray-200 rounded-lg shadow-sm">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                    <i class="fa-solid fa-id-badge mr-1"></i>ID
                  </th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                    <i class="fa-solid fa-signature mr-1"></i>Tên
                  </th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                    <i class="fa-solid fa-calendar mr-1"></i>Tuổi
                  </th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                    <i class="fa-solid fa-venus-mars mr-1"></i>Giới tính
                  </th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                    <i class="fa-solid fa-map-marker-alt mr-1"></i>Nơi ở
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200">
                ${people.map((person, index) => `
                  <tr class="hover:bg-gray-50 transition-colors">
                    <td class="px-4 py-3 whitespace-nowrap">
                      <span class="font-mono text-sm font-semibold text-blue-600">${person.class_id}</span>
                    </td>
                    <td class="px-4 py-3 whitespace-nowrap">
                      <span class="text-sm font-medium text-gray-900">${person.ten}</span>
                    </td>
                    <td class="px-4 py-3 whitespace-nowrap">
                      <span class="text-sm text-gray-600">${person.tuoi}</span>
                    </td>
                    <td class="px-4 py-3 whitespace-nowrap">
                      <span class="text-sm text-gray-600">${person.gioitinh}</span>
                    </td>
                    <td class="px-4 py-3">
                      <span class="text-sm text-gray-600">${person.noio}</span>
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        `;
        
        // Create pagination controls
        const paginationHtml = createPaginationControls('nguoi', nguoiSearchState);
        
        const resultContainer = document.getElementById(resultId);
        resultContainer.innerHTML = `
          <div class="mb-4 flex justify-between items-center">
            <div class="text-sm text-gray-600 flex items-center gap-2">
              <i class="fa-solid fa-info-circle"></i>
              Hiển thị ${people.length} / ${nguoiSearchState.totalResults} người
            </div>
            <div class="text-sm text-gray-500">
              Trang ${nguoiSearchState.currentPage} / ${nguoiSearchState.totalPages}
            </div>
          </div>
          ${tableHtml}
          ${paginationHtml}
        `;
        
        // Show success snackbar
        if (window.showSnackbar) {
          window.showSnackbar(`Tìm thấy ${nguoiSearchState.totalResults} người`, 'success');
        }
        
        // Update external pagination controls
        updatePaginationControls('nguoi', nguoiSearchState.currentPage, nguoiSearchState.totalPages);
    })
    .catch(err => {
        console.error('Error searching people:', err);
        window.UIUtils.showApiResult(resultId, { error: err.message || 'Lỗi kết nối đến server. Vui lòng thử lại sau.' });
        
        // Show error snackbar
        if (window.showSnackbar) {
          window.showSnackbar('Có lỗi xảy ra khi tìm kiếm', 'error');
        }
    });
}

function callGetAllNguoi(page = 1) {
  const resultId = 'searchNguoiResult';
  
  // Update state
  nguoiSearchState.currentQuery = '';
  nguoiSearchState.currentPage = page;
  
  // Show snackbar for starting process
  if (window.showSnackbar) {
    window.showSnackbar('Đang tải danh sách tất cả người...', 'info');
  }
  
  window.UIUtils.showLoading(resultId, true);
  
  // Add pagination parameters
  const params = new URLSearchParams();
  params.append('page', page);
  params.append('page_size', nguoiSearchState.pageSize);
  
  fetch(`${window.API_CONFIG.host}/list_nguoi?${params.toString()}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(res => res.json())
    .then(data => {
        const resultEl = document.getElementById(resultId);
        
        if (data.error) {
            window.UIUtils.showEmptyState(resultId, 
              'Không thể tải danh sách', 
              data.error || 'Có lỗi xảy ra khi tải danh sách người.',
              'fa-exclamation-triangle'
            );
            return;
        }
        
        // API returns { results: { nguoi_list: [...], total: number } }
        const apiData = data.results || {};
        const people = apiData.nguoi_list || [];
        
        // Update pagination state
        nguoiSearchState.totalResults = apiData.total || 0;
        nguoiSearchState.totalPages = Math.ceil(nguoiSearchState.totalResults / nguoiSearchState.pageSize);
        
        if (people.length === 0) {
            window.UIUtils.showEmptyState(resultId, 
              'Danh sách trống', 
              'Chưa có người nào trong hệ thống.',
              'fa-users'
            );
            return;
        }
        
        // Create table HTML (same as callSearchNguoi)
        const tableHtml = `
          <div class="overflow-x-auto">
            <table class="min-w-full bg-white border border-gray-200 rounded-lg shadow-sm">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                    <i class="fa-solid fa-id-badge mr-1"></i>ID
                  </th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                    <i class="fa-solid fa-signature mr-1"></i>Tên
                  </th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                    <i class="fa-solid fa-calendar mr-1"></i>Tuổi
                  </th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                    <i class="fa-solid fa-venus-mars mr-1"></i>Giới tính
                  </th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                    <i class="fa-solid fa-map-marker-alt mr-1"></i>Nơi ở
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200">
                ${people.map((person, index) => `
                  <tr class="hover:bg-gray-50 transition-colors">
                    <td class="px-4 py-3 whitespace-nowrap">
                      <span class="font-mono text-sm font-semibold text-blue-600">${person.class_id}</span>
                    </td>
                    <td class="px-4 py-3 whitespace-nowrap">
                      <span class="text-sm font-medium text-gray-900">${person.ten}</span>
                    </td>
                    <td class="px-4 py-3 whitespace-nowrap">
                      <span class="text-sm text-gray-600">${person.tuoi}</span>
                    </td>
                    <td class="px-4 py-3 whitespace-nowrap">
                      <span class="text-sm text-gray-600">${person.gioitinh}</span>
                    </td>
                    <td class="px-4 py-3">
                      <span class="text-sm text-gray-600">${person.noio}</span>
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        `;
        
        // Create pagination controls
        const paginationHtml = createPaginationControls('nguoi', nguoiSearchState);
        
        resultEl.innerHTML = `
          <div class="mb-4 flex justify-between items-center">
            <div class="text-sm text-gray-600 flex items-center gap-2">
              <i class="fa-solid fa-info-circle"></i>
              Hiển thị ${people.length} / ${nguoiSearchState.totalResults} người
            </div>
            <div class="text-sm text-gray-500">
              Trang ${nguoiSearchState.currentPage} / ${nguoiSearchState.totalPages}
            </div>
          </div>
          ${tableHtml}
          ${paginationHtml}
        `;
            
        // Show success snackbar
        if (window.showSnackbar) {
          window.showSnackbar(`Đã tải ${nguoiSearchState.totalResults} người`, 'success');
        }
        
        // Update external pagination controls
        updatePaginationControls('nguoi', nguoiSearchState.currentPage, nguoiSearchState.totalPages);
    })
    .catch(err => {
        console.error('Error loading people list:', err);
        window.UIUtils.showApiResult(resultId, { error: err.message || 'Lỗi kết nối đến server. Vui lòng thử lại sau.' });
        
        // Show error snackbar
        if (window.showSnackbar) {
          window.showSnackbar('Có lỗi xảy ra khi tải danh sách người', 'error');
        }
    });
}

function callGetAllImages() {
  const resultId = 'searchNguoiResult';
  
  // Show snackbar for starting process
  if (window.showSnackbar) {
    window.showSnackbar('Đang tải danh sách tất cả ảnh...', 'info');
  }
  
  window.UIUtils.showLoading(resultId, true);
  
  window.APIUtils.callProtectedApi('/images', 'GET')
    .then(result => {
        if (result.success) {
            const images = result.data || [];
            
            if (images.length === 0) {
                window.UIUtils.showEmptyState(resultId, 
                  'Danh sách ảnh trống', 
                  'Chưa có ảnh nào trong hệ thống.',
                  'fa-images'
                );
                return;
            }
            
            // Display results
            let html = images.map(image => `
              <div class="bg-white border border-gray-200 rounded-lg shadow-sm p-4 mb-4 transition-all duration-300 hover:shadow-xl hover:border-green-300">
                <div class="font-semibold text-green-700 flex items-center gap-2 mb-2">
                  <i class="fa-solid fa-image"></i>
                  Image ID: ${image.id}
                </div>
                <div class="text-sm text-gray-600 flex items-center gap-2">
                  <i class="fa-solid fa-folder"></i>
                  Đường dẫn: <span class="font-mono bg-gray-100 px-2 py-1 rounded">${image.image_path}</span>
                </div>
                <div class="text-sm text-gray-600 flex items-center gap-2">
                  <i class="fa-solid fa-tag"></i>
                  Class ID: <span class="font-mono bg-gray-100 px-2 py-1 rounded">${image.class_id}</span>
                </div>
                ${image.nguoi ? `
                  <div class="mt-3 pt-3 border-t border-gray-200">
                    <div class="font-bold text-gray-800 flex items-center gap-2 mb-2">
                      <i class="fa-solid fa-user"></i>
                      Thông tin người:
                    </div>
                    <div class="grid grid-cols-2 gap-2 text-sm text-gray-700">
                      <div class="flex items-center gap-2">
                        <i class="fa-solid fa-signature text-blue-500"></i>
                        Tên: <span class="font-semibold">${image.nguoi.ten}</span>
                      </div>
                      <div class="flex items-center gap-2">
                        <i class="fa-solid fa-calendar text-green-500"></i>
                        Tuổi: <span class="font-semibold">${image.nguoi.tuoi}</span>
                      </div>
                    </div>
                  </div>
                ` : ''}
              </div>
            `).join('');
            
            const resultEl = document.getElementById(resultId);
            resultEl.innerHTML = `
              <div class="mb-4 text-sm text-gray-600 flex items-center gap-2">
                <i class="fa-solid fa-info-circle"></i>
                Tổng cộng ${images.length} ảnh trong hệ thống
              </div>
              ${html}
            `;
            
            // Show success snackbar
            if (window.showSnackbar) {
              window.showSnackbar(`Đã tải ${images.length} ảnh`, 'success');
            }
        } else {
            window.UIUtils.showApiResult(resultId, { error: result.message || 'Có lỗi xảy ra khi tải danh sách ảnh.' });
        }
    })
    .catch(err => {
        window.UIUtils.showApiResult(resultId, { error: err.message || String(err) });
    });
}

function callSearchEmbedding(page = 1) {
  const classId = document.getElementById('searchEmbeddingInput')?.value?.trim();
  const resultId = 'searchEmbeddingResult';
  
  // Update state
  embeddingSearchState.currentQuery = classId || '';
  embeddingSearchState.currentPage = page;
  
  // Show snackbar for starting process
  if (window.showSnackbar) {
    window.showSnackbar('Đang tìm kiếm embedding...', 'info');
  }
  
  window.UIUtils.showLoading(resultId, true);
  
  // Build query parameters
  const params = new URLSearchParams();
  if (classId) {
    params.append('query', classId);  // API expects 'query' parameter, not 'class_id'
  }
  params.append('page', page);
  params.append('page_size', embeddingSearchState.pageSize);
  
  fetch(`${window.API_CONFIG.host}/search_embeddings?${params.toString()}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(res => res.json())
    .then(data => {
        console.log('Search embeddings response:', data);  // Debug log
        const resultEl = document.getElementById(resultId);
        
        if (data.error) {
            window.UIUtils.showEmptyState(resultId, 
              'Không thể tìm kiếm', 
              data.error || 'Có lỗi xảy ra khi tìm kiếm embedding.',
              'fa-exclamation-triangle'
            );
            return;
        }
        
        const embeddings = data.results || [];  // API returns { results: [...] }
        
        // Update pagination state
        embeddingSearchState.totalResults = data.total || 0;
        embeddingSearchState.totalPages = data.total_pages || 0;
        
        if (embeddings.length === 0) {
            window.UIUtils.showEmptyState(resultId, 
              'Không tìm thấy kết quả', 
              classId ? `Không tìm thấy embedding cho query: ${classId}` : 'Không có embedding nào trong hệ thống.',
              'fa-search'
            );
            return;
        }
        
        // Create table HTML
        const tableHtml = `
          <div class="overflow-x-auto">
            <table class="min-w-full bg-white border border-gray-200 rounded-lg shadow-sm">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                    <i class="fa-solid fa-tag mr-1"></i>Class ID
                  </th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                    <i class="fa-solid fa-fingerprint mr-1"></i>Image ID
                  </th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                    <i class="fa-solid fa-folder-open mr-1"></i>Image Path
                  </th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200">
                ${embeddings.map((embedding, index) => `
                  <tr class="hover:bg-gray-50 transition-colors">
                    <td class="px-4 py-3 whitespace-nowrap">
                      <span class="font-mono text-sm font-semibold text-green-600">${embedding.class_id}</span>
                    </td>
                    <td class="px-4 py-3 whitespace-nowrap">
                      <span class="font-mono text-sm bg-gray-100 px-2 py-1 rounded">${embedding.image_id}</span>
                    </td>
                    <td class="px-4 py-3">
                      <span class="font-mono text-xs text-gray-600 break-all">${embedding.image_path || 'N/A'}</span>
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        `;
        
        // Create pagination controls
        const paginationHtml = createPaginationControls('embedding', embeddingSearchState);
        
        resultEl.innerHTML = `
          <div class="mb-4 flex justify-between items-center">
            <div class="text-sm text-gray-600 flex items-center gap-2">
              <i class="fa-solid fa-info-circle"></i>
              Hiển thị ${embeddings.length} / ${embeddingSearchState.totalResults} embedding(s)
            </div>
            <div class="text-sm text-gray-500">
              Trang ${embeddingSearchState.currentPage} / ${embeddingSearchState.totalPages}
            </div>
          </div>
          ${tableHtml}
          ${paginationHtml}
        `;
        
        // Show success snackbar
        if (window.showSnackbar) {
          window.showSnackbar(`Tìm thấy ${embeddingSearchState.totalResults} embedding${embeddingSearchState.totalResults > 1 ? 's' : ''}`, 'success');
        }
        
        // Update external pagination controls
        updatePaginationControls('embedding', embeddingSearchState.currentPage, embeddingSearchState.totalPages);
    })
    .catch(err => {
        console.error('Error searching embeddings:', err);
        window.UIUtils.showApiResult(resultId, { error: err.message || 'Lỗi kết nối đến server. Vui lòng thử lại sau.' });
        
        // Show error snackbar
        if (window.showSnackbar) {
          window.showSnackbar('Có lỗi xảy ra khi tìm kiếm embedding', 'error');
        }
    });
}

// Create pagination controls
function createPaginationControls(type, state) {
  const { currentPage, totalPages } = state;
  
  return `
    <div class="mt-6 flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6 rounded-lg">
      <div class="flex flex-1 justify-between sm:hidden">
        <button 
          ${currentPage <= 1 ? 'disabled' : ''} 
          onclick="${type === 'embedding' ? 'navigateEmbeddingPage' : 'navigateNguoiPage'}(${currentPage - 1})"
          class="relative inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
          Trước
        </button>
        <button 
          ${currentPage >= totalPages ? 'disabled' : ''} 
          onclick="${type === 'embedding' ? 'navigateEmbeddingPage' : 'navigateNguoiPage'}(${currentPage + 1})"
          class="relative ml-3 inline-flex items-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
          Sau
        </button>
      </div>
      <div class="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
        <div class="flex items-center gap-4">
          <p class="text-sm text-gray-700">
            Trang <span class="font-medium">${currentPage}</span> trên <span class="font-medium">${totalPages}</span>
          </p>
          <div class="flex items-center gap-2">
            <label class="text-sm text-gray-600">Đi đến trang:</label>
            <input 
              type="number" 
              min="1" 
              max="${totalPages}" 
              value="${currentPage}"
              onkeypress="if(event.key==='Enter') ${type === 'embedding' ? 'navigateEmbeddingPage' : 'navigateNguoiPage'}(parseInt(this.value))"
              class="w-16 px-2 py-1 text-sm border border-gray-300 rounded focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500">
          </div>
        </div>
        <div>
          <nav class="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
            <button 
              ${currentPage <= 1 ? 'disabled' : ''} 
              onclick="${type === 'embedding' ? 'navigateEmbeddingPage' : 'navigateNguoiPage'}(${currentPage - 1})"
              class="relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 disabled:opacity-50 disabled:cursor-not-allowed">
              <i class="fa-solid fa-chevron-left"></i>
            </button>
            <button 
              ${currentPage >= totalPages ? 'disabled' : ''} 
              onclick="${type === 'embedding' ? 'navigateEmbeddingPage' : 'navigateNguoiPage'}(${currentPage + 1})"
              class="relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0 disabled:opacity-50 disabled:cursor-not-allowed">
              <i class="fa-solid fa-chevron-right"></i>
            </button>
          </nav>
        </div>
      </div>
    </div>
  `;
}

// Navigation functions
function navigateEmbeddingPage(page) {
  if (page >= 1 && page <= embeddingSearchState.totalPages) {
    callSearchEmbedding(page);
  }
}

function navigateNguoiPage(page) {
  if (page >= 1 && page <= nguoiSearchState.totalPages) {
    callSearchNguoi(page);
  }
}

// Export to global scope
window.SearchPage = {
  callSearchNguoi,
  callGetAllNguoi,
  callGetAllImages,
  callSearchEmbedding
};

// Export navigation functions to global scope for button onclick
window.navigateEmbeddingPage = navigateEmbeddingPage;
window.navigateNguoiPage = navigateNguoiPage;

// Export pagination states to global scope
window.embeddingSearchState = embeddingSearchState;
window.nguoiSearchState = nguoiSearchState;

// Helper function to show/hide pagination controls
function togglePaginationControls(type, show) {
  const controlsId = type === 'nguoi' ? 'nguoiPaginationControls' : 'embeddingPaginationControls';
  const controls = document.getElementById(controlsId);
  
  if (controls) {
    if (show) {
      controls.classList.remove('hidden');
    } else {
      controls.classList.add('hidden');
    }
  }
}

// Helper function to update pagination controls
function updatePaginationControls(type, currentPage, totalPages) {
  // Update page indicator
  if (window.updatePageIndicator) {
    window.updatePageIndicator(type, currentPage, totalPages);
  }
  
  // Update page input max value
  const inputId = type === 'nguoi' ? 'nguoiPageInput' : 'embeddingPageInput';
  const pageInput = document.getElementById(inputId);
  if (pageInput) {
    pageInput.max = totalPages;
    pageInput.value = currentPage;
  }
  
  // Show pagination controls if there are multiple pages
  togglePaginationControls(type, totalPages > 1);
}

// Export helper functions
window.togglePaginationControls = togglePaginationControls;
window.updatePaginationControls = updatePaginationControls;
