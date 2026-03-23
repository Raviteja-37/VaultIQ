import { useState, useRef, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { sendMessage } from '../api/chat';
import { raiseTicket } from '../api/tickets';
import Navbar from '../components/layout/Navbar';

const DOMAINS = [
  { value: null, label: '🌐 All Domains' },
  { value: 'sop', label: '📋 SOPs' },
  { value: 'compliance', label: '⚖️ Compliance' },
  { value: 'hr', label: '👥 HR Policies' },
  { value: 'public', label: '📢 Public' },
];

function ConfidenceBar({ score }) {
  const color =
    score >= 70 ? 'bg-green-500' : score >= 50 ? 'bg-yellow-500' : 'bg-red-500';
  const label = score >= 70 ? 'High' : score >= 50 ? 'Medium' : 'Low';
  return (
    <div className="mt-2">
      <div className="flex items-center justify-between mb-1">
        <span className="text-xs text-gray-500">Confidence</span>
        <span className="text-xs text-gray-400">
          {score}% · {label}
        </span>
      </div>
      <div className="h-1 bg-gray-700 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all ${color}`}
          style={{ width: `${score}%` }}
        />
      </div>
    </div>
  );
}

function Message({ msg, onRaiseTicket }) {
  const [ticketRaised, setTicketRaised] = useState(false);
  const [raising, setRaising] = useState(false);

  const handleRaiseTicket = async () => {
    setRaising(true);
    try {
      const ticket = await onRaiseTicket(msg);
      setTicketRaised(ticket);
    } finally {
      setRaising(false);
    }
  };

  if (msg.role === 'user')
    return (
      <div className="flex justify-end mb-4">
        <div className="bg-cyan-500 text-gray-950 rounded-2xl rounded-tr-sm px-4 py-2.5 max-w-xl text-sm font-medium">
          {msg.content}
        </div>
      </div>
    );

  return (
    <div className="flex justify-start mb-4">
      <div className="max-w-2xl w-full">
        <div
          className={`rounded-2xl rounded-tl-sm px-4 py-3 text-sm text-gray-200 leading-relaxed
          ${
            msg.is_restricted
              ? 'bg-red-500/10 border border-red-500/20'
              : 'bg-gray-800 border border-gray-700'
          }`}
        >
          {msg.is_restricted && (
            <div className="flex items-center gap-2 text-red-400 text-xs font-medium mb-2">
              <span>🔒</span> Confidential — Access Restricted
            </div>
          )}

          <p>{msg.content}</p>

          {/* Sources */}
          {msg.sources?.length > 0 && (
            <div className="mt-3 pt-3 border-t border-gray-700">
              <p className="text-xs text-gray-500 mb-2">Sources cited:</p>
              {msg.sources.map((s, i) => (
                <div
                  key={i}
                  className="flex items-center gap-2 text-xs text-cyan-400 mb-1"
                >
                  <span>📄</span>
                  <span>
                    {s.document} · Page {s.page} · {s.version} · {s.score}%
                  </span>
                </div>
              ))}
            </div>
          )}

          {/* Confidence */}
          {!msg.is_restricted && msg.confidence > 0 && (
            <ConfidenceBar score={msg.confidence} />
          )}

          {/* Raise Ticket */}
          {msg.raise_ticket && !ticketRaised && (
            <div className="mt-3 pt-3 border-t border-gray-700">
              <p className="text-xs text-yellow-400 mb-2">
                ⚠️ I couldn't find a confident answer. Would you like to raise a
                support ticket?
              </p>
              <button
                onClick={handleRaiseTicket}
                disabled={raising}
                className="bg-yellow-500/10 hover:bg-yellow-500/20 border border-yellow-500/20 text-yellow-400 text-xs px-3 py-1.5 rounded-lg transition-colors"
              >
                {raising
                  ? 'Raising ticket...'
                  : '🎫 Yes, raise a support ticket'}
              </button>
            </div>
          )}

          {ticketRaised && (
            <div className="mt-3 pt-3 border-t border-gray-700">
              <div className="bg-green-500/10 border border-green-500/20 rounded-lg px-3 py-2">
                <p className="text-green-400 text-xs font-medium">
                  ✅ Ticket raised: {ticketRaised.ticket_number}
                </p>
                <p className="text-gray-500 text-xs mt-0.5">
                  Assigned to: {ticketRaised.assigned_team}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function ChatPage() {
  const { user } = useAuth();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [domain, setDomain] = useState(null);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMsg = { role: 'user', content: input };
    const history = messages.map((m) => ({ role: m.role, content: m.content }));
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await sendMessage(input, domain, history);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: res.answer,
          sources: res.sources,
          confidence: res.confidence,
          is_restricted: res.is_restricted,
          raise_ticket: res.raise_ticket,
          low_confidence: res.low_confidence,
          original_query: input,
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, something went wrong. Please try again.',
          sources: [],
          confidence: 0,
          is_restricted: false,
          raise_ticket: false,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleRaiseTicket = async (msg) => {
    const history = messages.map((m) => ({ role: m.role, content: m.content }));
    return await raiseTicket(msg.original_query, history, msg.confidence);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 flex flex-col">
      <Navbar />
      <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full px-4 py-6">
        {/* Domain Selector */}
        {user?.role !== 'customer' && (
          <div className="flex items-center gap-2 mb-6">
            <span className="text-gray-500 text-xs">Domain:</span>
            {DOMAINS.map((d) => (
              <button
                key={String(d.value)}
                onClick={() => setDomain(d.value)}
                className={`text-xs px-3 py-1.5 rounded-full border transition-colors
                  ${
                    domain === d.value
                      ? 'bg-cyan-500/10 border-cyan-500/30 text-cyan-400'
                      : 'bg-gray-800 border-gray-700 text-gray-400 hover:text-white'
                  }`}
              >
                {d.label}
              </button>
            ))}
          </div>
        )}

        {/* Messages */}
        <div className="flex-1 overflow-y-auto">
          {messages.length === 0 && (
            <div className="text-center py-20">
              <div className="text-4xl mb-4">🏦</div>
              <h2 className="text-white font-semibold text-xl mb-2">
                Welcome, {user?.full_name}
              </h2>
              <p className="text-gray-500 text-sm max-w-md mx-auto">
                Ask me anything about banking policies, SOPs, compliance rules,
                or procedures. I'll find the answer from the knowledge base and
                cite my sources.
              </p>
              <div className="mt-6 flex flex-wrap gap-2 justify-center">
                {[
                  'What documents are needed for KYC?',
                  'How to handle a NACH mandate failure?',
                  'What is the exception handling process?',
                  'When must KYC be renewed?',
                ].map((q) => (
                  <button
                    key={q}
                    onClick={() => setInput(q)}
                    className="bg-gray-800 hover:bg-gray-700 border border-gray-700 text-gray-400 text-xs px-3 py-2 rounded-lg transition-colors"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg, i) => (
            <Message key={i} msg={msg} onRaiseTicket={handleRaiseTicket} />
          ))}

          {loading && (
            <div className="flex justify-start mb-4">
              <div className="bg-gray-800 border border-gray-700 rounded-2xl rounded-tl-sm px-4 py-3">
                <div className="flex items-center gap-2">
                  <div
                    className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-bounce"
                    style={{ animationDelay: '0ms' }}
                  />
                  <div
                    className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-bounce"
                    style={{ animationDelay: '150ms' }}
                  />
                  <div
                    className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-bounce"
                    style={{ animationDelay: '300ms' }}
                  />
                </div>
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="mt-4 bg-gray-900 border border-gray-700 rounded-2xl p-3 flex items-end gap-3">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask anything about banking policies, SOPs, compliance..."
            rows={1}
            className="flex-1 bg-transparent text-white text-sm resize-none focus:outline-none placeholder-gray-600 leading-relaxed"
            style={{ maxHeight: '120px' }}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || loading}
            className="bg-cyan-500 hover:bg-cyan-400 disabled:bg-gray-700 disabled:text-gray-500 text-gray-950 font-semibold text-sm px-4 py-2 rounded-xl transition-colors flex-shrink-0"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
