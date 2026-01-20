import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Unauthorized from './pages/Unauthorized';
import AdminDashboard from './pages/admin/AdminDashboard';
import FacultyManagement from './pages/admin/FacultyManagement';
import AdminReports from './pages/admin/AdminReports';
import FacultyDashboard from './pages/faculty/FacultyDashboard';
import UploadAttendance from './pages/faculty/UploadAttendance';
import AttendanceResults from './pages/faculty/AttendanceResults';
import FacultyReports from './pages/faculty/FacultyReports';
import ProtectedRoute from './components/ProtectedRoute';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/unauthorized" element={<Unauthorized />} />
        <Route
          path="/admin/dashboard"
          element={
            <ProtectedRoute role="admin">
              <AdminDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/faculty"
          element={
            <ProtectedRoute role="admin">
              <FacultyManagement />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin/reports"
          element={
            <ProtectedRoute role="admin">
              <AdminReports />
            </ProtectedRoute>
          }
        />
        <Route
          path="/faculty/dashboard"
          element={
            <ProtectedRoute role="faculty">
              <FacultyDashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/faculty/upload"
          element={
            <ProtectedRoute role="faculty">
              <UploadAttendance />
            </ProtectedRoute>
          }
        />
        <Route
          path="/faculty/results"
          element={
            <ProtectedRoute role="faculty">
              <AttendanceResults />
            </ProtectedRoute>
          }
        />
        <Route
          path="/faculty/reports"
          element={
            <ProtectedRoute role="faculty">
              <FacultyReports />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;