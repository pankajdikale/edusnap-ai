import { useState } from 'react';
import Header from '../../components/Header';
import Card from '../../components/Card';
import Toast from '../../components/Toast';
import Loader from '../../components/Loader';
import { addFaculty, deleteFaculty } from '../../services/api';

const FacultyManagement = () => {
  const [addForm, setAddForm] = useState({ username: '', name: '', email: '', department: '', year: '', password: '' });
  const [deleteForm, setDeleteForm] = useState({ email: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' } | null>(null);

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await addFaculty(addForm);
      setToast({ message: 'Faculty added successfully', type: 'success' });
      setAddForm({ username: '', name: '', email: '', department: '', year: '', password: '' });
    } catch (error: any) {
      setToast({ message: error.message || 'Failed to add faculty', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await deleteFaculty(deleteForm);
      setToast({ message: 'Faculty deleted successfully', type: 'success' });
      setDeleteForm({ email: '', password: '' });
    } catch (error: any) {
      setToast({ message: error.message || 'Failed to delete faculty', type: 'error' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Header />
      <div className="container">
        <h2>Faculty Management</h2>
        <Card>
          <h3>Add Faculty</h3>
          <form onSubmit={handleAdd}>
            <div className="form-group">
              <label>Username</label>
              <input value={addForm.username} onChange={(e) => setAddForm({ ...addForm, username: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>Name</label>
              <input value={addForm.name} onChange={(e) => setAddForm({ ...addForm, name: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>Email</label>
              <input type="email" value={addForm.email} onChange={(e) => setAddForm({ ...addForm, email: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>Department</label>
              <input value={addForm.department} onChange={(e) => setAddForm({ ...addForm, department: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>Year</label>
              <input value={addForm.year} onChange={(e) => setAddForm({ ...addForm, year: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>Password</label>
              <input type="password" value={addForm.password} onChange={(e) => setAddForm({ ...addForm, password: e.target.value })} required />
            </div>
            <button type="submit" className="button" disabled={loading}>
              {loading ? <Loader /> : 'Add Faculty'}
            </button>
          </form>
        </Card>
        <Card>
          <h3>Delete Faculty</h3>
          <form onSubmit={handleDelete}>
            <div className="form-group">
              <label>Email</label>
              <input type="email" value={deleteForm.email} onChange={(e) => setDeleteForm({ ...deleteForm, email: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>Password</label>
              <input type="password" value={deleteForm.password} onChange={(e) => setDeleteForm({ ...deleteForm, password: e.target.value })} required />
            </div>
            <button type="submit" className="button" disabled={loading}>
              {loading ? <Loader /> : 'Delete Faculty'}
            </button>
          </form>
        </Card>
      </div>
      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
    </div>
  );
};

export default FacultyManagement;