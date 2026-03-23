import api from './axios';

export const raiseTicket = async (query, chatHistory, confidence) => {
  const res = await api.post('/tickets/raise', {
    query,
    chat_history: chatHistory || [],
    confidence,
  });
  return res.data;
};

export const getMyTickets = async () => {
  const res = await api.get('/tickets/my');
  return res.data;
};

export const getAllTickets = async () => {
  const res = await api.get('/tickets/all');
  return res.data;
};

export const updateTicket = async (ticketId, status, resolutionNote) => {
  const res = await api.patch(`/tickets/${ticketId}`, {
    status,
    resolution_note: resolutionNote,
  });
  return res.data;
};
