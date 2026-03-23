import { useEffect, useState } from 'react';
import Navbar from '../components/layout/Navbar';
import {
  getAuditLogs,
  getRestrictedQueries,
  getUnresolvedQueries,
} from '../api/audit';

const TABS = ['All Queries', 'Restricted', 'Unresolved'];

function LogRow({ log }) {
  return (
    <tr className="border-b border-gray-800 hover:bg-gray-800/50 transition-colors">
      <td className="py-3 px-4 text-xs text-gray-500">
        {new Date(log.timestamp).toLocaleString()}
      </td>
      <td className="py-3 px-4 text-xs text-gray-300">{log.user_email}</td>
      <td className="py-3 px-4">
        <span className="text-xs bg-gray-800 border border-gray-700 text-gray-400 px-2 py-0.5 rounded-full">
          {log.user_role}
        </span>
      </td>
      <td className="py-3 px-4 text-xs text-gray-300 max-w-xs truncate">
        {log.query}
      </td>
      <td className="py-3 px-4 text-xs text-gray-400">
        {log.domain || 'general'}
      </td>
      <td className="py-3 px-4 text-xs">
        <span
          className={`font-medium ${
            log.confidence >= 70
              ? 'text-green-400'
              : log.confidence >= 50
                ? 'text-yellow-400'
                : 'text-red-400'
          }`}
        >
          {log.confidence}%
        </span>
      </td>
      <td className="py-3 px-4">
        {log.is_restricted && (
          <span className="text-xs bg-red-500/10 border border-red-500/20 text-red-400 px-2 py-0.5 rounded-full">
            🔒 Restricted
          </span>
        )}
        {log.low_confidence && !log.is_restricted && (
          <span className="text-xs bg-yellow-500/10 border border-yellow-500/20 text-yellow-400 px-2 py-0.5 rounded-full">
            ⚠️ Low Confidence
          </span>
        )}
        {!log.is_restricted && !log.low_confidence && (
          <span className="text-xs bg-green-500/10 border border-green-500/20 text-green-400 px-2 py-0.5 rounded-full">
            ✅ Normal
          </span>
        )}
      </td>
    </tr>
  );
}

export default function AuditPage() {
  const [activeTab, setActiveTab] = useState(0);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    const fetcher = [getAuditLogs, getRestrictedQueries, getUnresolvedQueries][
      activeTab
    ];
    fetcher()
      .then(setLogs)
      .finally(() => setLoading(false));
  }, [activeTab]);

  return (
    <div className="min-h-screen bg-gray-950">
      <Navbar />
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="mb-6">
          <h1 className="text-white font-bold text-2xl">Audit Dashboard</h1>
          <p className="text-gray-500 text-sm mt-1">
            Complete query history and compliance trail
          </p>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6">
          {TABS.map((tab, i) => (
            <button
              key={tab}
              onClick={() => setActiveTab(i)}
              className={`text-sm px-4 py-2 rounded-lg border transition-colors ${
                activeTab === i
                  ? 'bg-cyan-500/10 border-cyan-500/30 text-cyan-400'
                  : 'bg-gray-800 border-gray-700 text-gray-400 hover:text-white'
              }`}
            >
              {tab}
              {i === 1 && (
                <span className="ml-2 bg-red-500/20 text-red-400 text-xs px-1.5 py-0.5 rounded-full">
                  !
                </span>
              )}
            </button>
          ))}
        </div>

        {/* Table */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-800">
                {[
                  'Timestamp',
                  'User',
                  'Role',
                  'Query',
                  'Domain',
                  'Confidence',
                  'Status',
                ].map((h) => (
                  <th
                    key={h}
                    className="text-left py-3 px-4 text-xs text-gray-500 font-medium uppercase tracking-wider"
                  >
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td
                    colSpan={7}
                    className="text-center py-12 text-gray-600 text-sm"
                  >
                    Loading...
                  </td>
                </tr>
              ) : logs.length === 0 ? (
                <tr>
                  <td
                    colSpan={7}
                    className="text-center py-12 text-gray-600 text-sm"
                  >
                    No logs found
                  </td>
                </tr>
              ) : (
                logs.map((log) => <LogRow key={log.id} log={log} />)
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
