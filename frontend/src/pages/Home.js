import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/App.css';

const Home = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div className="home-page">
      <section className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">
            Unleash Your Imagination with 
            <span className="gradient-text"> StoryGenie</span>
          </h1>
          <p className="hero-subtitle">
            Create magical, AI-powered stories in multiple languages. 
            From fantasy adventures to mysterious tales, bring your ideas to life with just a prompt.
          </p>
          
          {isAuthenticated ? (
            <div className="hero-actions">
              <Link to="/create" className="btn btn-primary btn-large">
                Create Your Story
              </Link>
              <Link to="/dashboard" className="btn btn-secondary btn-large">
                Go to Dashboard
              </Link>
            </div>
          ) : (
            <div className="hero-actions">
              <Link to="/register" className="btn btn-primary btn-large">
                Start Creating Free
              </Link>
              <Link to="/login" className="btn btn-secondary btn-large">
                Sign In
              </Link>
            </div>
          )}
        </div>
        
        <div className="hero-visual">
          <div className="story-preview">
            <div className="preview-header">
              <div className="preview-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
            <div className="preview-content">
              <h4>The Lost Kingdom of Eldoria</h4>
              <p>In a world where magic flowed like rivers, young Elara discovered she could speak to ancient stones...</p>
            </div>
          </div>
        </div>
      </section>

      <section className="features-section">
        <div className="container">
          <h2 className="section-title">Why Choose StoryGenie?</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🌍</div>
              <h3>Multi-Lingual</h3>
              <p>Create stories in English, Hindi, Telugu and more languages coming soon</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">⚡</div>
              <h3>AI Powered</h3>
              <p>Advanced AI transforms your prompts into engaging, well-crafted stories</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">🎭</div>
              <h3>Multiple Genres</h3>
              <p>Fantasy, Mystery, Romance, Sci-Fi and more - explore endless possibilities</p>
            </div>
            
            <div className="feature-card">
              <div className="feature-icon">📚</div>
              <h3>Your Library</h3>
              <p>Save, organize, and revisit all your created stories in one place</p>
            </div>
          </div>
        </div>
      </section>

      <section className="cta-section">
        <div className="container">
          <h2>Ready to Create Magic?</h2>
          <p>Join thousands of storytellers bringing their ideas to life</p>
          {!isAuthenticated && (
            <Link to="/register" className="btn btn-primary btn-large">
              Join StoryGenie Today
            </Link>
          )}
        </div>
      </section>
    </div>
  );
};

export default Home;