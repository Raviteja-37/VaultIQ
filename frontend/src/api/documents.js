import api from './axios';

export const uploadDocument = async (file, namespace, version) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('namespace', namespace);
  formData.append('version', version);
  const res = await api.post('/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return res.data;
};

export const listDocuments = async () => {
  const res = await api.get('/documents/list');
  return res.data;
};

export const deleteDocument = async (namespace, filename) => {
  const res = await api.delete(
    `/documents/delete?namespace=${namespace}&filename=${filename}`,
  );
  return res.data;
};
