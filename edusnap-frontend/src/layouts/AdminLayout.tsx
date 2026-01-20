import type { ReactNode } from 'react';
import { Link } from 'react-router-dom';

interface AdminLayoutProps {
  children: ReactNode;
}

const AdminLayout: React.FC<AdminLayoutProps> = ({ children }) => {
  return (
    <div className="flex min-h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-blue-800 text-white p-4">
        <h2 className="text-xl font-bold mb-6">Admin Panel</h2>
        <nav className="space-y-4">
          <Link to="/admin/dashboard" className="block hover:bg-blue-700 p-2 rounded">
            Dashboard
          </Link>
          <Link to="/admin/reports" className="block hover:bg-blue-700 p-2 rounded">
            Reports
          </Link>
          <Link to="/admin/faculty" className="block hover:bg-blue-700 p-2 rounded">
            Faculty Management
          </Link>
        </nav>
      </aside>
      {/* Main Content */}
      <main className="flex-1 p-6">
        {children}
      </main>
    </div>
  );
};

export default AdminLayout;