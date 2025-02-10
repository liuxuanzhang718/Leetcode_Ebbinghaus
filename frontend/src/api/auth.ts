import apiClient from './client';

interface RegisterData {
  email: string;
  password: string;
  notification_time?: string;
  timezone?: string;
}

interface LoginData {
  username: string;  // email
  password: string;
}

interface ResetPasswordData {
  email: string;
  old_password: string;
  new_password: string;
}

interface UpdateUserData {
  notification_time?: string;
  timezone?: string;
}

export const register = async (data: RegisterData) => {
  const response = await apiClient.post('/auth/register', data);
  return response.data;
};

export const login = async (data: LoginData) => {
  const formData = new FormData();
  formData.append('username', data.username);
  formData.append('password', data.password);
  
  const response = await apiClient.post('/auth/token', formData);
  return response.data;
};

export const resetPassword = async (data: ResetPasswordData) => {
  const response = await apiClient.post('/auth/reset-password', data);
  return response.data;
};

export const updateUser = async (data: UpdateUserData) => {
  const response = await apiClient.put('/auth/users/me', data);
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await apiClient.get('/auth/users/me');
  return response.data;
}; 