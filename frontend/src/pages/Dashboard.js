import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { storiesAPI } from '../services/api';
import StoryList from '../components/Stories/StoryList';
import LoadingSpinner from '../components/Layout/LoadingSpinner';
import '../styles/Stories.css';

const Dashboard = () => {
  const { user } = useAuth();
  const [stories, setStories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    totalStories: 0,
    totalWords: 0,
    favoriteStories: 0
  });

  useEffect(() => {
    fetchUserStories();
  }, []);

  const fetchUserStories = async () => {
    try {
      setLoading(true);
      const response = await storiesAPI.getAll(0, 6);
      const storiesData = response.data.stories;
      setStories(storiesData);
      
      // Calculate basic stats
      const totalWords = storiesData.reduce((sum, story) => sum + (story.word_count || 0), 0);
      const favoriteStories = storiesData.filter(story => story.is_favorite).length;
      
      setStats({
        totalStories: storiesData.length,
        totalWords,
        favoriteStories
      });
    } catch (error) {
      console.error('Error fetching stories:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Welcome back, {user?.username}! 👋</h1>
        <p>Continue your storytelling journey</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📚</div>
          <div className="stat-info">
            <h3>{stats.totalStories}</h3>
            <p>Total Stories</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">📝</div>
          <div className="stat-info">
            <h3>{stats.totalWords}</h3>
            <p>Words Written</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">⭐</div>
          <div className="stat-info">
            <h3>{stats.favoriteStories}</h3>
            <p>Favorites</p>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon">🚀</div>
          <div className="stat-info">
            <Link to="/create" className="btn btn-primary">
              Create New
            </Link>
            <p>Start New Story</p>
          </div>
        </div>
      </div>

      <section className="recent-stories">
        <div className="section-header">
          <h2>Recent Stories</h2>
          <Link to="/history" className="view-all-link">
            View All →
          </Link>
        </div>
        
        {loading ? (
          <LoadingSpinner text="Loading your stories..." />
        ) : (
          <StoryList stories={stories} loading={false} />
        )}
        
        {!loading && stories.length === 0 && (
          <div className="empty-state">
            <div className="empty-icon">📖</div>
            <h3>No stories yet</h3>
            <p>Create your first story and start your storytelling journey!</p>
            <Link to="/create" className="btn btn-primary">
              Create Your First Story
            </Link>
          </div>
        )}
      </section>
    </div>
  );
};

export default Dashboard;