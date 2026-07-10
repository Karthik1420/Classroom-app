import React, { useState, useEffect } from 'react';
import toast from 'react-hot-toast';
import Navbar from '../../components/Navbar/Navbar';
import ClassroomCard from '../../components/UI/ClassroomCard';
import Modal from '../../components/UI/Modal';
import Loader from '../../components/UI/Loader';
import { getJoinedClassrooms, joinClassroom } from '../../services/classroomService';
import styles from '../TeacherDashboard/TeacherDashboard.module.css';

const StudentDashboard = () => {
  const [classrooms, setClassrooms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [classroomCode, setClassroomCode] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchClassrooms();
  }, []);

  const fetchClassrooms = async () => {
    try {
      const data = await getJoinedClassrooms();
      setClassrooms(data);
    } catch (error) {
      toast.error('Failed to fetch enrolled classrooms');
    } finally {
      setLoading(false);
    }
  };

  const handleJoin = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await joinClassroom(classroomCode);
      toast.success('Successfully joined classroom!');
      setIsModalOpen(false);
      setClassroomCode('');
      // Refresh list
      fetchClassrooms();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to join classroom. Check code.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className={styles.dashboardLayout}>
      <Navbar />
      <main className="container" style={{ marginTop: '2rem' }}>
        <div className={styles.header}>
          <h2>Enrolled Classrooms</h2>
          <button className="btn-primary" onClick={() => setIsModalOpen(true)}>
            + Join Class
          </button>
        </div>

        {loading ? (
          <Loader />
        ) : classrooms.length === 0 ? (
          <div className={styles.emptyState}>
            <h3>No classrooms yet</h3>
            <p>Click "Join Class" and enter the 8-character code from your teacher.</p>
          </div>
        ) : (
          <div className={styles.grid}>
            {classrooms.map((c) => (
              <ClassroomCard key={c.id} classroom={c} role="student" />
            ))}
          </div>
        )}
      </main>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Join Class">
        <form onSubmit={handleJoin}>
          <div className="form-group">
            <label className="form-label">Class Code (8 characters)</label>
            <input 
              type="text" 
              className="form-input" 
              value={classroomCode}
              onChange={(e) => setClassroomCode(e.target.value)}
              minLength={8}
              maxLength={8}
              required 
            />
          </div>
          <button type="submit" className="btn-primary" style={{ width: '100%' }} disabled={submitting}>
            {submitting ? 'Joining...' : 'Join'}
          </button>
        </form>
      </Modal>
    </div>
  );
};

export default StudentDashboard;
