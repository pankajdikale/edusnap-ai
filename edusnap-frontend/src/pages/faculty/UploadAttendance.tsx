import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../../components/Header';
import Card from '../../components/Card';
import Toast from '../../components/Toast';
import Loader from '../../components/Loader';
import { uploadAttendance } from '../../services/api';

const UploadAttendance = () => {
  const [form, setForm] = useState({ image: null as File | null, department: '', year: '', course: '', subject: '' });
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await uploadAttendance(form);
      navigate('/faculty/results');
    } catch (error: any) {
      setToast({ message: error.message || 'Upload failed', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Header />
      <div className="container">
        <h2>Upload Attendance</h2>
        <Card>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Image</label>
              <input type="file" accept="image/*" onChange={(e) => setForm({ ...form, image: e.target.files?.[0] || null })} required />
            </div>
            <div className="form-group">
              <label>Department</label>
              <input value={form.department} onChange={(e) => setForm({ ...form, department: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>Year</label>
              <input value={form.year} onChange={(e) => setForm({ ...form, year: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>Course</label>
              <input value={form.course} onChange={(e) => setForm({ ...form, course: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>Subject</label>
              <input value={form.subject} onChange={(e) => setForm({ ...form, subject: e.target.value })} required />
            </div>
            <button type="submit" className="button" disabled={loading}>
              {loading ? <Loader /> : 'Get Report'}
            </button>
          </form>
        </Card>
      </div>
      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
    </div>
  );
};

export default UploadAttendance;