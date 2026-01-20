import type { ReactNode } from 'react';
import { Link } from 'react-router-dom';

interface FacultyLayoutProps {
  children: ReactNode;
}

const FacultyLayout: React.FC<FacultyLayoutProps> = ({ children }) => {
  return (
    <div className="flex min-h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className="w-64 bg-green-800 text-white p-4">
        <h2 className="text-xl font-bold mb-6">Faculty Panel</h2>
        <nav className="space-y-4">
          <Link to="/faculty/dashboard" className="block hover:bg-green-700 p-2 rounded">
            Dashboard
          </Link>
          <Link to="/faculty/attendance" className="block hover:bg-green-700 p-2 rounded">
            Upload Attendance
          </Link>
          <Link to="/faculty/attendance/results" className="block hover:bg-green-700 p-2 rounded">
            Attendance Results
          </Link>
          <Link to="/faculty/reports" className="block hover:bg-green-700 p-2 rounded">
            Reports
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

export default FacultyLayout;