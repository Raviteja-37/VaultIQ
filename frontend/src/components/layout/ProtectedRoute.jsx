import { Navigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export default function ProtectedRoute({ children, roles }) {
  const { user, loading } = useAuth();

  if (loading)
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <div className="text-gray-400 text-sm">Loading...</div>
      </div>
    );

  if (!user) return <Navigate to="/login" replace />;

  if (roles && !roles.includes(user.role))
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-400 text-4xl mb-4">⛔</div>
          <div className="text-white text-lg font-semibold">Access Denied</div>
          <div className="text-gray-400 text-sm mt-2">
            Your role ({user.role}) doesn't have permission to view this page.
          </div>
        </div>
      </div>
    );

  return children;
}
