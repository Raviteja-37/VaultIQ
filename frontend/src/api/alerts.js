import api from './axios';

export const getAlerts = async () => {
  const res = await api.get('/alerts/');
  return res.data;
};

export const markAlertReviewed = async (alertId) => {
  const res = await api.patch(`/alerts/${alertId}/review`);
  return res.data;
};
