import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api',  // 统一使用 /api 前缀
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      if (!config.headers) {
        config.headers = {};
      }
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 添加响应拦截器处理认证错误
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // 清除无效的 token
      localStorage.removeItem('token');
      // 重定向到登录页面
      window.location.href = '/auth/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient; 