import { useEffect, useState } from 'react';
import Navbar from '../components/layout/Navbar';
import { getMyTickets, getAllTickets, updateTicket } from '../api/tickets';
import { useAuth } from '../context/AuthContext';

const STATUS_COLORS = {
  open: 'bg-yellow-500/10 border-yellow-500/20 text-yellow-400',
  inprogress: 'bg-blue-500/10 border-blue-500/20 text-blue-400',
  resolved: 'bg-green-500/10 border-green-500/20 text-green-400',
  closed: 'bg-gray-500/10 border-gray-500/20 text-gray-400',
};

export default function TicketsPage() {
  const { user, hasRole } = useAuth();
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(null);
  const [note, setNote] = useState('');

  const isStaff = hasRole('ops_staff', 'manager', 'admin', 'executive');

  useEffect(() => {
    const fetcher = isStaff ? getAllTickets : getMyTickets;
    fetcher()
      .then(setTickets)
      .finally(() => setLoading(false));
  }, []);

  const handleUpdate = async (ticketId, status) => {
    const updated = await updateTicket(ticketId, status, note);
    setTickets((prev) => prev.map((t) => (t.id === ticketId ? updated : t)));
    setSelected(null);
    setNote('');
  };

  return (
    <div className="min-h-screen bg-gray-950">
      <Navbar />
      <div className="max-w-5xl mx-auto px-6 py-8">
        <div className="mb-6">
          <h1 className="text-white font-bold text-2xl">
            {isStaff ? 'All Support Tickets' : 'My Tickets'}
          </h1>
          <p className="text-gray-500 text-sm mt-1">
            {isStaff
              ? 'View and manage all customer support tickets'
              : 'Track your support requests and their status'}
          </p>
        </div>

        {loading ? (
          <div className="text-center py-20 text-gray-600">Loading...</div>
        ) : tickets.length === 0 ? (
          <div className="text-center py-20">
            <div className="text-4xl mb-4">🎫</div>
            <p className="text-gray-500 text-sm">No tickets found</p>
          </div>
        ) : (
          <div className="space-y-3">
            {tickets.map((ticket) => (
              <div
                key={ticket.id}
                className="bg-gray-900 border border-gray-800 rounded-xl p-5"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-cyan-400 font-mono text-sm font-bold">
                        {ticket.ticket_number}
                      </span>
                      <span
                        className={`text-xs border px-2 py-0.5 rounded-full ${STATUS_COLORS[ticket.status]}`}
                      >
                        {ticket.status}
                      </span>
                      <span className="text-xs bg-gray-800 border border-gray-700 text-gray-400 px-2 py-0.5 rounded-full">
                        {ticket.category}
                      </span>
                    </div>
                    <p className="text-gray-300 text-sm mb-2">
                      "{ticket.original_query}"
                    </p>
                    <div className="flex items-center gap-4 text-xs text-gray-600">
                      {isStaff && <span>👤 {ticket.customer_email}</span>}
                      <span>👥 {ticket.assigned_team}</span>
                      <span>
                        🕐 {new Date(ticket.created_at).toLocaleString()}
                      </span>
                    </div>
                    {ticket.resolution_note && (
                      <div className="mt-3 bg-green-500/5 border border-green-500/10 rounded-lg px-3 py-2">
                        <p className="text-green-400 text-xs">
                          Resolution: {ticket.resolution_note}
                        </p>
                      </div>
                    )}
                  </div>

                  {isStaff && ticket.status !== 'closed' && (
                    <div className="flex-shrink-0">
                      {selected === ticket.id ? (
                        <div className="space-y-2">
                          <textarea
                            value={note}
                            onChange={(e) => setNote(e.target.value)}
                            placeholder="Resolution note..."
                            className="bg-gray-800 border border-gray-700 text-white text-xs rounded-lg px-3 py-2 w-48 resize-none focus:outline-none"
                            rows={2}
                          />
                          <div className="flex gap-2">
                            <button
                              onClick={() =>
                                handleUpdate(ticket.id, 'resolved')
                              }
                              className="flex-1 bg-green-500/10 hover:bg-green-500/20 border border-green-500/20 text-green-400 text-xs px-2 py-1.5 rounded-lg transition-colors"
                            >
                              Resolve
                            </button>
                            <button
                              onClick={() =>
                                handleUpdate(ticket.id, 'inprogress')
                              }
                              className="flex-1 bg-blue-500/10 hover:bg-blue-500/20 border border-blue-500/20 text-blue-400 text-xs px-2 py-1.5 rounded-lg transition-colors"
                            >
                              In Progress
                            </button>
                          </div>
                          <button
                            onClick={() => setSelected(null)}
                            className="w-full text-gray-600 text-xs hover:text-gray-400 transition-colors"
                          >
                            Cancel
                          </button>
                        </div>
                      ) : (
                        <button
                          onClick={() => setSelected(ticket.id)}
                          className="bg-gray-800 hover:bg-gray-700 border border-gray-700 text-gray-400 hover:text-white text-xs px-3 py-1.5 rounded-lg transition-colors"
                        >
                          Update
                        </button>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
