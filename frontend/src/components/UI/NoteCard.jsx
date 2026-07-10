import React from 'react';
import { FileText, Download, ExternalLink } from 'lucide-react';
import Card from './Card';
import { getNoteViewUrl, getNoteDownloadUrl } from '../../services/noteService';
import styles from './NoteCard.module.css';

const NoteCard = ({ note }) => {
  // If file_name is missing, it means the metadata was created but file wasn't uploaded successfully
  const hasFile = Boolean(note.file_name);

  return (
    <Card className={styles.noteCard}>
      <div className={styles.icon}>
        <FileText size={32} color="var(--primary)" />
      </div>
      <div className={styles.content}>
        <h4 className={styles.title}>{note.title}</h4>
        {note.description && <p className={styles.description}>{note.description}</p>}
        <p className={styles.meta}>Uploaded: {new Date(note.created_at).toLocaleDateString()}</p>
      </div>
      <div className={styles.actions}>
        {hasFile ? (
          <>
            <a href={getNoteViewUrl(note.id)} target="_blank" rel="noopener noreferrer" className={styles.actionBtn}>
              <ExternalLink size={18} /> View
            </a>
            <a href={getNoteDownloadUrl(note.id)} download className={styles.actionBtn}>
              <Download size={18} /> Download
            </a>
          </>
        ) : (
          <span className={styles.missing}>File missing</span>
        )}
      </div>
    </Card>
  );
};
export default NoteCard;
