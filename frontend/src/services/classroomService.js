import api from './api';

export const createClassroom = async (classroomData) => {
  const response = await api.post('/classrooms/', classroomData);
  return response.data;
};

export const getTeacherClassrooms = async () => {
  const response = await api.get('/classrooms/');
  return response.data;
};

export const getJoinedClassrooms = async () => {
  const response = await api.get('/classrooms/joined');
  return response.data;
};

export const joinClassroom = async (classroomCode) => {
  const response = await api.post('/classrooms/join', { classroom_code: classroomCode });
  return response.data;
};

export const getEnrolledStudents = async (classroomId) => {
  const response = await api.get(`/classrooms/${classroomId}/students`);
  return response.data;
};

// We don't have a direct "getClassroomDetails" endpoint, but we can usually find it in the list
// or we can fetch the students/notes which validates the classroom.
// Let's create a utility to find a classroom by fetching the list.
export const getClassroomDetails = async (classroomId, role) => {
  const list = role === 'teacher' ? await getTeacherClassrooms() : await getJoinedClassrooms();
  return list.find(c => c.id === parseInt(classroomId));
};
