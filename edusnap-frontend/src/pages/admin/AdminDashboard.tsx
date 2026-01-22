import { useNavigate } from 'react-router-dom';
import Header from '../../components/Header';
import Card from '../../components/Card';

const AdminDashboard = () => {
  const navigate = useNavigate();

  return (
    <div>
      <Header />
      <div className="container">
        <h2>Admin Dashboard</h2>
        <Card>
          <button className="button" onClick={() => navigate('/admin/faculty?action=add')}>Add Faculty</button>
          <button className="button" onClick={() => navigate('/admin/faculty?action=delete')}>Delete Faculty</button>
          <button className="button" onClick={() => navigate('/admin/reports')}>View Attendance Reports</button>
        </Card>
      </div>
    </div>
  );
};

export default AdminDashboard;