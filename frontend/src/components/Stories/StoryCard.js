import React from 'react';
import { Link } from 'react-router-dom';
import '../../styles/Stories.css';

const StoryCard = ({ story }) => {
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const getLanguageName = (code) => {
    const languages = {
      'en': 'English',
      'hi': 'Hindi',
      'te': 'Telugu'
    };
    return languages[code] || code;
  };

  return (
    <div className="story-card">
      <div className="story-card-header">
        <h3 className="story-title">{story.title}</h3>
        {story.is_favorite && <span className="favorite-badge">⭐</span>}
      </div>
      
      <div className="story-meta">
        <span className={`genre-tag genre-${story.genre}`}>
          {story.genre}
        </span>
        <span className="language-tag">
          {getLanguageName(story.language)}
        </span>
        <span className="length-tag">
          {story.length}
        </span>
      </div>

      <div className="story-stats">
        <span className="word-count">{story.word_count} words</span>
        <span className="created-date">{formatDate(story.created_at)}</span>
      </div>

      <div className="story-card-actions">
        <Link to={`/story/${story.id}`} className="btn btn-secondary">
          Read Story
        </Link>
      </div>
    </div>
  );
};

export default StoryCard;