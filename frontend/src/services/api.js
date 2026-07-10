import axios from 'axios';

const api = axios.create({
  baseURL: 'https://classroom-app-g38b.onrender.com/api/v1',
});

// Interceptor to attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export default api;
