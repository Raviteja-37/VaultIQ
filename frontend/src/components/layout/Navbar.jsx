import { useAuth } from '../../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

const ROLE_COLORS = {
  customer: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
  ops_staff: 'bg-green-500/10 text-green-400 border-green-500/20',
  compliance: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
  manager: 'bg-orange-500/10 text-orange-400 border-orange-500/20',
  admin: 'bg-purple-500/10 text-purple-400 border-purple-500/20',
  executive: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
};

const ROLE_LABELS = {
  customer: 'Customer',
  ops_staff: 'Ops Staff',
  compliance: 'Compliance',
  manager: 'Manager',
  admin: 'Admin',
  executive: 'Executive',
};

export default function Navbar() {
  const { user, logoutUser, hasRole } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logoutUser();
    navigate('/login');
  };

  return (
    <nav className="bg-gray-900 border-b border-gray-800 px-6 py-3 flex items-center justify-between">
      <div className="flex items-center gap-8">
        <Link
          to="/chat"
          className="text-white font-bold text-lg tracking-tight"
        >
          Vault<span className="text-cyan-400">IQ</span>
        </Link>
        <div className="flex items-center gap-1">
          <Link
            to="/chat"
            className="text-gray-400 hover:text-white text-sm px-3 py-1.5 rounded-md hover:bg-gray-800 transition-colors"
          >
            Chat
          </Link>
          {hasRole('manager', 'admin', 'executive', 'compliance') && (
            <Link
              to="/audit"
              className="text-gray-400 hover:text-white text-sm px-3 py-1.5 rounded-md hover:bg-gray-800 transition-colors"
            >
              Audit
            </Link>
          )}
          {hasRole('manager', 'admin', 'executive') && (
            <Link
              to="/alerts"
              className="text-gray-400 hover:text-white text-sm px-3 py-1.5 rounded-md hover:bg-gray-800 transition-colors"
            >
              Alerts
            </Link>
          )}
          {hasRole(
            'customer',
            'ops_staff',
            'manager',
            'admin',
            'executive',
          ) && (
            <Link
              to="/tickets"
              className="text-gray-400 hover:text-white text-sm px-3 py-1.5 rounded-md hover:bg-gray-800 transition-colors"
            >
              Tickets
            </Link>
          )}
          {hasRole('admin') && (
            <Link
              to="/admin"
              className="text-gray-400 hover:text-white text-sm px-3 py-1.5 rounded-md hover:bg-gray-800 transition-colors"
            >
              Admin
            </Link>
          )}
        </div>
      </div>
      <div className="flex items-center gap-3">
        <span
          className={`text-xs px-2.5 py-1 rounded-full border font-medium ${ROLE_COLORS[user?.role]}`}
        >
          {ROLE_LABELS[user?.role]}
        </span>
        <span className="text-gray-400 text-sm">{user?.full_name}</span>
        <button
          onClick={handleLogout}
          className="text-gray-500 hover:text-red-400 text-sm px-3 py-1.5 rounded-md hover:bg-gray-800 transition-colors"
        >
          Logout
        </button>
      </div>
    </nav>
  );
}
