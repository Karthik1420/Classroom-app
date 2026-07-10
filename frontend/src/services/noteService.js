import api from './api';

export const createNoteMetadata = async (noteData) => {
  const response = await api.post('/notes/', noteData);
  return response.data;
};

export const uploadNoteFile = async (noteId, file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post(`/notes/${noteId}/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  });
  return response.data;
};

export const getClassroomNotes = async (classroomId) => {
  const response = await api.get(`/notes/classroom/${classroomId}`);
  return response.data;
};

// Returns the URL for inline viewing
export const getNoteViewUrl = (noteId) => {
  return `${api.defaults.baseURL}/notes/${noteId}/file`;
};

// Returns the URL for downloading
export const getNoteDownloadUrl = (noteId) => {
  return `${api.defaults.baseURL}/notes/${noteId}/download`;
};
