import { Navigate } from 'react-router-dom';
import { useAuthStore } from '../stores/authStore';

interface ProtectedRouteProps {
  role: 'admin' | 'faculty';
  children: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ role, children }) => {
  const { isAuthenticated, role: userRole } = useAuthStore();  // Renamed to avoid conflict: store's 'role' is now 'userRole'

  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }

  if (userRole !== role) {  // Updated to use 'userRole' (which is store's 'role')
    return <Navigate to="/unauthorized" />;
  }

  return <>{children}</>;
};

export default ProtectedRoute;