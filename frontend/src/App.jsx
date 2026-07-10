import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';

import Login from './pages/Login/Login';
import Register from './pages/Register/Register';
import TeacherDashboard from './pages/TeacherDashboard/TeacherDashboard';
import TeacherClassroomDetails from './pages/TeacherDashboard/TeacherClassroomDetails';
import StudentDashboard from './pages/StudentDashboard/StudentDashboard';
import StudentClassroomDetails from './pages/StudentDashboard/StudentClassroomDetails';

const RootRedirect = () => {
  const { user, loading } = useAuth();
  
  if (loading) return null;
  if (!user) return <Navigate to="/login" replace />;
  
  return user.role === 'teacher' ? <Navigate to="/teacher/dashboard" replace /> : <Navigate to="/student/dashboard" replace />;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Toaster position="top-right" />
        <Routes>
          <Route path="/" element={<RootRedirect />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          <Route 
            path="/teacher/dashboard" 
            element={
              <ProtectedRoute allowedRoles={['teacher']}>
                <TeacherDashboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/teacher/classroom/:id" 
            element={
              <ProtectedRoute allowedRoles={['teacher']}>
                <TeacherClassroomDetails />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/student/dashboard" 
            element={
              <ProtectedRoute allowedRoles={['student']}>
                <StudentDashboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/student/classroom/:id" 
            element={
              <ProtectedRoute allowedRoles={['student']}>
                <StudentClassroomDetails />
              </ProtectedRoute>
            } 
          />
          
          {/* Fallback 404 Route */}
          <Route path="*" element={<div style={{padding: '4rem', textAlign: 'center'}}><h2>404 - Page Not Found</h2></div>} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
