import React from 'react';
import StoryCard from './StoryCard';
import '../../styles/Stories.css';

const StoryList = ({ stories, loading }) => {
  if (loading) {
    return (
      <div className="stories-loading">
        <div className="loading-spinner"></div>
        <p>Loading your stories...</p>
      </div>
    );
  }

  if (!stories || stories.length === 0) {
    return (
      <div className="no-stories">
        <div className="no-stories-icon">📝</div>
        <h3>No stories yet</h3>
        <p>Create your first story to get started!</p>
      </div>
    );
  }

  return (
    <div className="stories-grid">
      {stories.map((story) => (
        <StoryCard key={story.id} story={story} />
      ))}
    </div>
  );
};

export default StoryList;