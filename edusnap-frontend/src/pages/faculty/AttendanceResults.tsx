import { useState, useEffect } from 'react';
import Header from '../../components/Header';
import Card from '../../components/Card';
import Toast from '../../components/Toast';
import Loader from '../../components/Loader';
import { getAttendanceResults } from '../../services/api';

const AttendanceResults = () => {
  const [results, setResults] = useState<any>({ image: '', students: [] });
  const [latestImage, setLatestImage] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const data = await getAttendanceResults();
        setResults(data);
      } catch (error: any) {
        setToast({ message: error.message || 'Failed to load results', type: 'error' });
      } finally {
        setLoading(false);
      }
    };
    fetchResults();

    // Fetch latest image
    const fetchLatestImage = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/attendance/latest-image', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('auth-token')}`,
          },
        });
        if (response.ok) {
          const data = await response.json();
          setLatestImage(data.image);
        }
      } catch (error) {
        console.error('Failed to fetch latest image:', error);
      }
    };
    fetchLatestImage();
  }, []);

  const handleDownload = async (type: 'csv' | 'pdf') => {
    try {
      const response = await fetch(`http://localhost:8000/api/attendance/download/latest/${type}`, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('auth-token')}`,
        },
      });

      if (!response.ok) {
        throw new Error('Download failed');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `latest.${type}`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error: any) {
      setToast({ message: error.message || 'Download failed', type: 'error' });
    }
  };

  if (loading) return <Loader />;

  return (
    <div>
      <Header />
      <div className="container">
        <h2>Attendance Results</h2>
        <Card>
          <h3>Attendance Preview</h3>
          {latestImage && (
            <img src={`http://localhost:8000/static/attendance_outputs/${latestImage}`} alt="Attendance Preview" style={{ maxWidth: '100%' }} />
          )}
          <h3>Detected Students</h3>
          <ul>
            {results.students.map((student: any, index: number) => (
              <li key={index}>{student.name} - {student.rollNumber}</li>
            ))}
          </ul>
          <button className="button" onClick={() => handleDownload('pdf')}>Download PDF</button>
          <button className="button" onClick={() => handleDownload('csv')}>Download CSV</button>
        </Card>
      </div>
      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
    </div>
  );
};

export default AttendanceResults;