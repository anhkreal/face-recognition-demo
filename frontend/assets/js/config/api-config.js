/**
 * API Configuration Module
 * Handles API host detection and configuration
 */

// API Host Configuration
let apiHost = '';
if (window.location.hostname === 'localhost') {
  // Localhost: backend on port 8000
  apiHost = 'http://localhost:8000';
} else if (window.location.hostname === '172.16.8.184') {
  // Network: backend on port 8000, frontend on different port
  apiHost = 'http://172.16.8.184:8000';
} else {
  // Default fallback
  apiHost = 'http://127.0.0.1:8000';
}

// Export configuration
window.API_CONFIG = {
  host: apiHost,
  endpoints: {
    auth: {
      login: '/auth/login'
    },
    public: {
      query: '/query',
      predict: '/predict',
      listNguoi: '/list_nguoi'
    },
    protected: {
      addEmbedding: '/add_embedding',
      editEmbedding: '/edit_embedding',
      deleteImage: '/delete_image',
      deleteClass: '/delete_class',
      resetIndex: '/reset_index',
      searchEmbeddings: '/search_embeddings'
    }
  }
};

console.log('API Config loaded:', window.API_CONFIG);
