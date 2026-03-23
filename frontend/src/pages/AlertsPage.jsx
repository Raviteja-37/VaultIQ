import { useEffect, useState } from 'react';
import Navbar from '../components/layout/Navbar';
import { getAlerts, markAlertReviewed } from '../api/alerts';

export default function AlertsPage() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAlerts()
      .then(setAlerts)
      .finally(() => setLoading(false));
  }, []);

  const handleReview = async (id) => {
    await markAlertReviewed(id);
    setAlerts((prev) =>
      prev.map((a) => (a.id === id ? { ...a, is_reviewed: true } : a)),
    );
  };

  return (
    <div className="min-h-screen bg-gray-950">
      <Navbar />
      <div className="max-w-5xl mx-auto px-6 py-8">
        <div className="mb-6">
          <h1 className="text-white font-bold text-2xl">Security Alerts</h1>
          <p className="text-gray-500 text-sm mt-1">
            Triggered when users attempt to access restricted information
          </p>
        </div>

        {loading ? (
          <div className="text-center py-20 text-gray-600">Loading...</div>
        ) : alerts.length === 0 ? (
          <div className="text-center py-20">
            <div className="text-4xl mb-4">✅</div>
            <p className="text-gray-500 text-sm">
              No security alerts — all clear
            </p>
          </div>
        ) : (
          <div className="space-y-3">
            {alerts.map((alert) => (
              <div
                key={alert.id}
                className={`bg-gray-900 border rounded-xl p-5 transition-all ${
                  alert.is_reviewed
                    ? 'border-gray-800 opacity-60'
                    : 'border-red-500/30 bg-red-500/5'
                }`}
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className="text-red-400 text-sm">🚨</span>
                      <span className="text-white font-medium text-sm">
                        {alert.triggered_by_email}
                      </span>
                      <span className="text-xs bg-gray-800 border border-gray-700 text-gray-400 px-2 py-0.5 rounded-full">
                        {alert.triggered_by_role}
                      </span>
                      {alert.department && (
                        <span className="text-xs text-gray-600">
                          · {alert.department}
                        </span>
                      )}
                    </div>
                    <p className="text-gray-300 text-sm mb-2">
                      <span className="text-gray-500">Query: </span>"
                      {alert.query}"
                    </p>
                    <div className="flex items-center gap-4">
                      <span className="text-xs text-red-400">
                        Keywords: {alert.restricted_keywords}
                      </span>
                      <span className="text-xs text-gray-600">
                        {new Date(alert.timestamp).toLocaleString()}
                      </span>
                    </div>
                  </div>
                  <div className="flex-shrink-0">
                    {alert.is_reviewed ? (
                      <span className="text-xs bg-green-500/10 border border-green-500/20 text-green-400 px-3 py-1.5 rounded-lg">
                        Reviewed
                      </span>
                    ) : (
                      <button
                        onClick={() => handleReview(alert.id)}
                        className="text-xs bg-gray-800 hover:bg-gray-700 border border-gray-700 text-gray-400 hover:text-white px-3 py-1.5 rounded-lg transition-colors"
                      >
                        Mark Reviewed
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
