import api from './api';

export const login = async (email, password) => {
  // FastAPI's OAuth2PasswordRequestForm requires x-www-form-urlencoded format
  const formData = new URLSearchParams();
  formData.append('username', email);
  formData.append('password', password);

  const response = await api.post('/login/access-token', formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  });
  return response.data;
};

// Optional: verify token validity against backend
export const testToken = async () => {
  const response = await api.get('/test-token');
  return response.data;
};
