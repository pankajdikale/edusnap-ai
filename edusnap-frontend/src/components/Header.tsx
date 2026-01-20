import { useAuthStore } from '../stores/authStore';
import { useNavigate, Link } from 'react-router-dom';
import logo from '../assets/edusnap-logo.png'; // Add your small logo image to src/assets/

const Header = () => {
  const { isAuthenticated, role, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="header">
      <div className="logo">
        <Link to="/" style={{ textDecoration: 'none', color: 'inherit', display: 'flex', alignItems: 'center' }}>
          <img src={logo} alt="EduSnap Logo" style={{ width: '40px', height: 'auto', marginRight: '10px' }} />
          EduSnap AI
        </Link>
      </div>
      {isAuthenticated && (
        <nav style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
          {role === 'admin' && (
            <>
              <Link to="/admin/dashboard" style={{ color: 'white', textDecoration: 'none', fontWeight: '500' }}>Dashboard</Link>
              <Link to="/admin/faculty" style={{ color: 'white', textDecoration: 'none', fontWeight: '500' }}>Faculty</Link>
              <Link to="/admin/reports" style={{ color: 'white', textDecoration: 'none', fontWeight: '500' }}>Reports</Link>
            </>
          )}
          {role === 'faculty' && (
            <>
              <Link to="/faculty/dashboard" style={{ color: 'white', textDecoration: 'none', fontWeight: '500' }}>Dashboard</Link>
              <Link to="/faculty/upload" style={{ color: 'white', textDecoration: 'none', fontWeight: '500' }}>Upload</Link>
              <Link to="/faculty/results" style={{ color: 'white', textDecoration: 'none', fontWeight: '500' }}>Results</Link>
              <Link to="/faculty/reports" style={{ color: 'white', textDecoration: 'none', fontWeight: '500' }}>Reports</Link>
            </>
          )}
          <button className="button" onClick={handleLogout} style={{ margin: '0' }}>Logout</button>
        </nav>
      )}
    </header>
  );
};

export default Header;