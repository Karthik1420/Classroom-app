import React, { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import Navbar from '../../components/Navbar/Navbar';
import ClassroomCard from '../../components/UI/ClassroomCard';
import Modal from '../../components/UI/Modal';
import Loader from '../../components/UI/Loader';
import { getTeacherClassrooms, createClassroom } from '../../services/classroomService';
import styles from './TeacherDashboard.module.css';

const TeacherDashboard = () => {
  const [classrooms, setClassrooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState({ classroom_name: '', description: '' });
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchClassrooms();
  }, []);

  const fetchClassrooms = async () => {
    try {
      const data = await getTeacherClassrooms();
      setClassrooms(data);
    } catch (error) {
      toast.error('Failed to fetch classrooms');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const newClassroom = await createClassroom(formData);
      setClassrooms([newClassroom, ...classrooms]);
      setIsModalOpen(false);
      setFormData({ classroom_name: '', description: '' });
      toast.success('Classroom created successfully!');
    } catch (error) {
      toast.error('Failed to create classroom');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className={styles.dashboardLayout}>
      <Navbar />
      <main className="container" style={{ marginTop: '2rem' }}>
        <div className={styles.header}>
          <h2>My Classrooms</h2>
          <button className="btn-primary" onClick={() => setIsModalOpen(true)}>
            + Create Class
          </button>
        </div>

        {loading ? (
          <Loader />
        ) : classrooms.length === 0 ? (
          <div className={styles.emptyState}>
            <h3>No classrooms yet</h3>
            <p>Create a classroom to get started with your students.</p>
          </div>
        ) : (
          <div className={styles.grid}>
            {classrooms.map((c) => (
              <ClassroomCard key={c.id} classroom={c} role="teacher" />
            ))}
          </div>
        )}
      </main>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Create Class">
        <form onSubmit={handleCreate}>
          <div className="form-group">
            <label className="form-label">Class Name (required)</label>
            <input 
              type="text" 
              className="form-input" 
              value={formData.classroom_name}
              onChange={(e) => setFormData({...formData, classroom_name: e.target.value})}
              required 
            />
          </div>
          <div className="form-group">
            <label className="form-label">Description (optional)</label>
            <textarea 
              className="form-input" 
              rows="3"
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
            />
          </div>
          <button type="submit" className="btn-primary" style={{ width: '100%' }} disabled={submitting}>
            {submitting ? 'Creating...' : 'Create'}
          </button>
        </form>
      </Modal>
    </div>
  );
};

export default TeacherDashboard;
