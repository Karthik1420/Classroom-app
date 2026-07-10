import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import Navbar from '../../components/Navbar/Navbar';
import NoteCard from '../../components/UI/NoteCard';
import Loader from '../../components/UI/Loader';
import { getClassroomDetails } from '../../services/classroomService';
import { getClassroomNotes } from '../../services/noteService';
import styles from '../TeacherDashboard/TeacherClassroomDetails.module.css'; // Reusing Teacher CSS

const StudentClassroomDetails = () => {
  const { id } = useParams();
  const [classroom, setClassroom] = useState(null);
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, [id]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [classData, notesData] = await Promise.all([
        getClassroomDetails(id, 'student'),
        getClassroomNotes(id)
      ]);
      setClassroom(classData);
      setNotes(notesData);
    } catch (error) {
      toast.error('Error loading classroom details or you are not enrolled.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <><Navbar /><Loader /></>;
  if (!classroom) return <><Navbar /><div className="container" style={{padding:'4rem', textAlign:'center'}}>Classroom not found.</div></>;

  return (
    <div className={styles.layout}>
      <Navbar />
      <div className={styles.hero}>
        <div className="container">
          <h1 className={styles.heroTitle}>{classroom.classroom_name}</h1>
          <p className={styles.heroSubtitle}>Teacher: <strong>{classroom.teacher_id}</strong></p>
        </div>
      </div>

      <div className={`container ${styles.mainContent}`}>
        <div className={styles.notesHeader}>
          <h3>Classroom Materials</h3>
        </div>
        {notes.length === 0 ? (
          <div className={styles.emptyState}>No notes uploaded yet.</div>
        ) : (
          notes.map(note => <NoteCard key={note.id} note={note} />)
        )}
      </div>
    </div>
  );
};

export default StudentClassroomDetails;
