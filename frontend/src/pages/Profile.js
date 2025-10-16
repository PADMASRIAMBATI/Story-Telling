import React from 'react';
import { useAuth } from '../context/AuthContext';
import '../styles/App.css';

const Profile = () => {
  const { user } = useAuth();

  const getLanguageName = (code) => {
    const languages = {
      'en': 'English',
      'hi': 'Hindi',
      'te': 'Telugu'
    };
    return languages[code] || code;
  };

  return (
    <div className="profile-page">
      <div className="page-header">
        <h1>Your Profile</h1>
        <p>Manage your account information</p>
      </div>

      <div className="profile-card">
        <div className="profile-header">
          <div className="profile-avatar">
            {user?.username?.charAt(0).toUpperCase()}
          </div>
          <div className="profile-info">
            <h2>{user?.username}</h2>
            <p className="profile-email">{user?.email}</p>
          </div>
        </div>

        <div className="profile-details">
          <div className="detail-item">
            <label>Username</label>
            <span>{user?.username}</span>
          </div>
          
          <div className="detail-item">
            <label>Email</label>
            <span>{user?.email}</span>
          </div>
          
          <div className="detail-item">
            <label>Preferred Language</label>
            <span>{getLanguageName(user?.preferred_language)}</span>
          </div>
          
          <div className="detail-item">
            <label>Stories Created</label>
            <span>{user?.story_count || 0}</span>
          </div>
          
          <div className="detail-item">
            <label>Member Since</label>
            <span>Recently joined</span>
          </div>
        </div>
      </div>

      <div className="profile-actions">
        <h3>Account Actions</h3>
        <div className="action-buttons">
          <button className="btn btn-secondary">Edit Profile</button>
          <button className="btn btn-secondary">Change Password</button>
          <button className="btn btn-danger">Delete Account</button>
        </div>
      </div>
    </div>
  );
};

export default Profile;