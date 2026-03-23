import api from './axios';

export const sendMessage = async (query, domain, chatHistory) => {
  const res = await api.post('/chat/', {
    query,
    domain: domain || null,
    chat_history: chatHistory || [],
  });
  return res.data;
};
