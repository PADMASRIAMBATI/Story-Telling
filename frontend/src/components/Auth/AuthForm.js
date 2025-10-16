import React from 'react';
import Input from '../Common/Input';
import Button from '../Common/Button';
import '../../styles/Auth.css';

const AuthForm = ({
  type,
  formData,
  onChange,
  onSubmit,
  loading,
  error
}) => {
  const isLogin = type === 'login';

  return (
    <form className="auth-form" onSubmit={onSubmit}>
      <h2>{isLogin ? 'Welcome Back' : 'Join StoryGenie'}</h2>
      <p className="auth-subtitle">
        {isLogin ? 'Sign in to your account' : 'Create your account to start generating stories'}
      </p>

      {error && (
        <div className="error-banner">
          {error}
        </div>
      )}

      {!isLogin && (
        <Input
          label="Username"
          type="text"
          value={formData.username}
          onChange={(e) => onChange('username', e.target.value)}
          placeholder="Enter your username"
          required
        />
      )}

      <Input
        label="Email"
        type="email"
        value={formData.email}
        onChange={(e) => onChange('email', e.target.value)}
        placeholder="Enter your email"
        required
      />

      <Input
        label="Password"
        type="password"
        value={formData.password}
        onChange={(e) => onChange('password', e.target.value)}
        placeholder="Enter your password"
        required
      />

      {!isLogin && (
        <div className="input-group">
          <label className="input-label">Preferred Language</label>
          <select
            value={formData.preferred_language}
            onChange={(e) => onChange('preferred_language', e.target.value)}
            className="input-field"
          >
            <option value="en">English</option>
            <option value="hi">Hindi</option>
            <option value="te">Telugu</option>
          </select>
        </div>
      )}

      <Button 
        type="submit" 
        variant="primary" 
        loading={loading}
        className="auth-submit-btn"
      >
        {isLogin ? 'Sign In' : 'Create Account'}
      </Button>

      <p className="auth-switch">
        {isLogin ? "Don't have an account? " : "Already have an account? "}
        <a href={isLogin ? '/register' : '/login'} className="auth-link">
          {isLogin ? 'Sign up' : 'Sign in'}
        </a>
      </p>
    </form>
  );
};

export default AuthForm;