import api from './axios';

export const getAuditLogs = async (limit = 50, offset = 0) => {
  const res = await api.get(`/audit/logs?limit=${limit}&offset=${offset}`);
  return res.data;
};

export const getRestrictedQueries = async () => {
  const res = await api.get('/audit/restricted');
  return res.data;
};

export const getUnresolvedQueries = async () => {
  const res = await api.get('/audit/unresolved');
  return res.data;
};
