import React from 'react';
import { Link } from 'react-router-dom';
import styles from '../Login/Login.module.css';

const Register = () => {
  const handleSubmit = (e) => {
    e.preventDefault();
    alert("Backend registration is not implemented yet. Please use the dummy accounts provided (teacher@example.com / student@example.com).");
  };

  return (
    <div className={styles.loginContainer}>
      <div className={styles.loginCard}>
        <h2 className={styles.title}>Create your account</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Email</label>
            <input type="email" className="form-input" required />
          </div>
          <div className="form-group">
            <label className="form-label">Password</label>
            <input type="password" className="form-input" required />
          </div>
          <button type="submit" className={`btn-primary ${styles.submitBtn}`}>
            Register
          </button>
        </form>
        <div className={styles.linkText}>
          Already have an account? <Link to="/login" className={styles.link}>Sign in instead</Link>
        </div>
      </div>
    </div>
  );
};

export default Register;
