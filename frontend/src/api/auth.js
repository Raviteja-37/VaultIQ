import api from './axios';

export const login = async (email, password) => {
  const res = await api.post('/auth/login', { email, password });
  return res.data;
};

export const getMe = async () => {
  const res = await api.get('/auth/me');
  return res.data;
};

export const getUsers = async () => {
  const res = await api.get('/auth/users');
  return res.data;
};
