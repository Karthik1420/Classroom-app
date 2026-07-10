import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Upload } from 'lucide-react';
import Navbar from '../../components/Navbar/Navbar';
import NoteCard from '../../components/UI/NoteCard';
import Modal from '../../components/UI/Modal';
import Loader from '../../components/UI/Loader';
import { getClassroomDetails, getEnrolledStudents } from '../../services/classroomService';
import { getClassroomNotes, createNoteMetadata, uploadNoteFile } from '../../services/noteService';
import styles from './TeacherClassroomDetails.module.css';

const TeacherClassroomDetails = () => {
  const { id } = useParams();
  const [classroom, setClassroom] = useState(null);
  const [notes, setNotes] = useState([]);
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('notes'); // 'notes' or 'students'

  // Upload Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    fetchData();
  }, [id]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [classData, notesData, studentsData] = await Promise.all([
        getClassroomDetails(id, 'teacher'),
        getClassroomNotes(id),
        getEnrolledStudents(id)
      ]);
      setClassroom(classData);
      setNotes(notesData);
      setStudents(studentsData);
    } catch (error) {
      toast.error('Error loading classroom details');
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return toast.error('Please select a PDF file');
    if (file.type !== 'application/pdf') return toast.error('Only PDF files are allowed');

    setUploading(true);
    try {
      // Step 1: Create Metadata
      const noteMeta = await createNoteMetadata({
        title,
        description,
        classroom_id: parseInt(id)
      });

      // Step 2: Upload File
      const finalNote = await uploadNoteFile(noteMeta.id, file);
      
      setNotes([finalNote, ...notes]);
      setIsModalOpen(false);
      setTitle('');
      setDescription('');
      setFile(null);
      toast.success('Note uploaded successfully');
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to upload note');
    } finally {
      setUploading(false);
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
          <p className={styles.heroSubtitle}>Classroom Code: <strong>{classroom.classroom_code}</strong></p>
        </div>
      </div>

      <div className={`container ${styles.mainContent}`}>
        <div className={styles.tabs}>
          <button className={`${styles.tabBtn} ${activeTab === 'notes' ? styles.activeTab : ''}`} onClick={() => setActiveTab('notes')}>
            Stream & Notes
          </button>
          <button className={`${styles.tabBtn} ${activeTab === 'students' ? styles.activeTab : ''}`} onClick={() => setActiveTab('students')}>
            People ({students.length})
          </button>
        </div>

        <div className={styles.tabContent}>
          {activeTab === 'notes' ? (
            <div>
              <div className={styles.notesHeader}>
                <h3>Notes Feed</h3>
                <button className="btn-primary" onClick={() => setIsModalOpen(true)}>
                  <Upload size={16} style={{marginRight: '0.5rem', verticalAlign:'middle'}}/>
                  Upload PDF
                </button>
              </div>
              {notes.length === 0 ? (
                <div className={styles.emptyState}>No notes uploaded yet.</div>
              ) : (
                notes.map(note => <NoteCard key={note.id} note={note} />)
              )}
            </div>
          ) : (
            <div>
              <h3>Enrolled Students</h3>
              {students.length === 0 ? (
                <div className={styles.emptyState}>No students enrolled yet.</div>
              ) : (
                <div className={styles.studentList}>
                  {students.map(s => (
                    <div key={s.id} className={styles.studentItem}>
                      <div className={styles.studentAvatar}>{s.student_id.charAt(0).toUpperCase()}</div>
                      <span>{s.student_id}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Upload PDF Note">
        <form onSubmit={handleUpload}>
          <div className="form-group">
            <label className="form-label">Title</label>
            <input type="text" className="form-input" value={title} onChange={e => setTitle(e.target.value)} required />
          </div>
          <div className="form-group">
            <label className="form-label">Description (Optional)</label>
            <textarea className="form-input" rows="3" value={description} onChange={e => setDescription(e.target.value)} />
          </div>
          <div className="form-group">
            <label className="form-label">PDF File</label>
            <input type="file" accept="application/pdf" className="form-input" onChange={e => setFile(e.target.files[0])} required />
          </div>
          <button type="submit" className="btn-primary" style={{width: '100%'}} disabled={uploading}>
            {uploading ? 'Uploading...' : 'Upload'}
          </button>
        </form>
      </Modal>
    </div>
  );
};

export default TeacherClassroomDetails;
