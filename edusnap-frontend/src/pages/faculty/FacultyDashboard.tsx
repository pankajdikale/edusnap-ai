import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../../components/Header';
import Card from '../../components/Card';
import Modal from '../../components/Modal';
import Toast from '../../components/Toast';
import Loader from '../../components/Loader';
import { addStudent } from '../../services/api';

const FacultyDashboard = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [studentForm, setStudentForm] = useState({ name: '', rollNumber: '', department: '', semester: '', image: null as File | null });
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);
  const navigate = useNavigate();

  const handleAddStudent = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await addStudent(studentForm);
      setToast({ message: 'Student added successfully', type: 'success' });
      setStudentForm({ name: '', rollNumber: '', department: '', semester: '', image: null });
      setIsModalOpen(false);
    } catch (error: any) {
      console.error('Add Student Error:', error);  // Log full error for debugging
      setToast({ message: error.message || 'Failed to add student', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Header />
      <div className="container">
        <h2>Faculty Dashboard</h2>
        <Card>
          <button className="button" onClick={() => setIsModalOpen(true)}>Add Student</button>
          <button className="button" onClick={() => navigate('/faculty/upload')}>Upload Attendance</button>
        </Card>
      </div>
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
        <h3>Add Student</h3>
        <form onSubmit={handleAddStudent}>
          <div className="form-group">
            <label>Name</label>
            <input value={studentForm.name} onChange={(e) => setStudentForm({ ...studentForm, name: e.target.value })} required />
          </div>
          <div className="form-group">
            <label>Roll Number</label>
            <input value={studentForm.rollNumber} onChange={(e) => setStudentForm({ ...studentForm, rollNumber: e.target.value })} required />
          </div>
          <div className="form-group">
            <label>Department</label>
            <input value={studentForm.department} onChange={(e) => setStudentForm({ ...studentForm, department: e.target.value })} required />
          </div>
          <div className="form-group">
            <label>Semester</label>
            <input value={studentForm.semester} onChange={(e) => setStudentForm({ ...studentForm, semester: e.target.value })} required />
          </div>
          <div className="form-group">
            <label>Image</label>
            <input type="file" accept="image/*" onChange={(e) => setStudentForm({ ...studentForm, image: e.target.files?.[0] || null })} required />
          </div>
          <button type="submit" className="button" disabled={loading}>
            {loading ? <Loader /> : 'Add Student'}
          </button>
        </form>
      </Modal>
      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
    </div>
  );
};

export default FacultyDashboard;