import React from 'react';
import { Loader2 } from 'lucide-react';

const Loader = ({ center = true }) => {
  return (
    <div style={{ display: 'flex', justifyContent: center ? 'center' : 'flex-start', padding: '2rem' }}>
      <Loader2 className="spinner" size={32} color="var(--primary)" />
      <style>{`
        .spinner { animation: spin 1s linear infinite; }
        @keyframes spin { 100% { transform: rotate(360deg); } }
      `}</style>
    </div>
  );
};
export default Loader;
