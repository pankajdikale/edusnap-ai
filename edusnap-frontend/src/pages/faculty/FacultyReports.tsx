import Header from '../../components/Header';
import Card from '../../components/Card';
import Toast from '../../components/Toast';
import Loader from '../../components/Loader';
import { getFacultyReports } from '../../services/api';
import { useEffect, useState } from 'react';

const FacultyReports = () => {
  const [reports, setReports] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const data = await getFacultyReports();
        setReports(data);
      } catch (error: any) {
        setToast({ message: error.message || 'Failed to load reports', type: 'error' });
      } finally {
        setLoading(false);
      }
    };
    fetchReports();
  }, []);

  if (loading) return <Loader />;

  return (
    <div>
      <Header />
      <div className="container">
        <h2>Faculty Reports</h2>
        <Card>
          <table className="table">
            <thead>
              <tr>
                <th>Subject</th>
                <th>Attendance %</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {reports.map((report, index) => (
                <tr key={index}>
                  <td>{report.subject}</td>
                  <td>{report.attendance}</td>
                  <td>{report.date}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>
      </div>
      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
    </div>
  );
};

export default FacultyReports;