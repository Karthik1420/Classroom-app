import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Users } from 'lucide-react';
import Card from './Card';
import styles from './ClassroomCard.module.css';

const ClassroomCard = ({ classroom, role }) => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/${role}/classroom/${classroom.id}`);
  };

  return (
    <Card onClick={handleClick} className={styles.classroomCard}>
      <div className={styles.header}>
        <h3 className={styles.title}>{classroom.classroom_name}</h3>
        <p className={styles.subtitle}>Code: {classroom.classroom_code}</p>
      </div>
      <div className={styles.body}>
        {classroom.description && <p className={styles.description}>{classroom.description}</p>}
      </div>
      <div className={styles.footer}>
        <Users size={16} />
        <span>Owner: {classroom.teacher_id}</span>
      </div>
    </Card>
  );
};
export default ClassroomCard;
