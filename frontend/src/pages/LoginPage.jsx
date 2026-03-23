import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { login } from '../api/auth';

const DEMO_USERS = [
  { email: 'customer@demo.com', role: 'Customer', color: 'text-blue-400' },
  { email: 'ops@demo.com', role: 'Ops Staff', color: 'text-green-400' },
  {
    email: 'compliance@demo.com',
    role: 'Compliance',
    color: 'text-yellow-400',
  },
  { email: 'manager@demo.com', role: 'Manager', color: 'text-orange-400' },
  { email: 'admin@demo.com', role: 'Admin', color: 'text-purple-400' },
  { email: 'ceo@demo.com', role: 'Executive', color: 'text-amber-400' },
];

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { loginUser } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const data = await login(email, password);
      loginUser(data.user, data.access_token);
      navigate('/chat');
    } catch (err) {
      setError(
        err.response?.data?.detail || 'Login failed. Check your credentials.',
      );
    } finally {
      setLoading(false);
    }
  };

  const fillDemo = (demoEmail) => {
    setEmail(demoEmail);
    setPassword('demo1234');
    setError('');
  };

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white tracking-tight">
            Vault<span className="text-cyan-400">IQ</span>
          </h1>
          <p className="text-gray-500 text-sm mt-2">
            AI-Powered Banking Knowledge Assistant
          </p>
        </div>

        {/* Login Form */}
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-8">
          <h2 className="text-white font-semibold text-lg mb-6">
            Sign in to your account
          </h2>

          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="text-gray-400 text-sm block mb-1.5">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@company.com"
                required
                className="w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-cyan-500 transition-colors placeholder-gray-600"
              />
            </div>
            <div>
              <label className="text-gray-400 text-sm block mb-1.5">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="w-full bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:border-cyan-500 transition-colors placeholder-gray-600"
              />
            </div>

            {error && (
              <div className="bg-red-500/10 border border-red-500/20 text-red-400 text-sm rounded-lg px-4 py-2.5">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-cyan-500 hover:bg-cyan-400 disabled:bg-cyan-500/50 text-gray-950 font-semibold rounded-lg py-2.5 text-sm transition-colors"
            >
              {loading ? 'Signing in...' : 'Sign in'}
            </button>
          </form>

          {/* Demo Users */}
          <div className="mt-6 pt-6 border-t border-gray-800">
            <p className="text-gray-500 text-xs mb-3">
              Quick demo login — click any role:
            </p>
            <div className="grid grid-cols-2 gap-2">
              {DEMO_USERS.map((u) => (
                <button
                  key={u.email}
                  onClick={() => fillDemo(u.email)}
                  className="text-left bg-gray-800 hover:bg-gray-700 border border-gray-700 rounded-lg px-3 py-2 transition-colors"
                >
                  <div className={`text-xs font-medium ${u.color}`}>
                    {u.role}
                  </div>
                  <div className="text-gray-500 text-xs truncate">
                    {u.email}
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
