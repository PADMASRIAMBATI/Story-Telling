import React from 'react';
import '../../styles/Stories.css';

const StoryDetail = ({ story, loading }) => {
  if (loading) {
    return (
      <div className="story-detail-loading">
        <div className="loading-spinner"></div>
        <p>Loading story...</p>
      </div>
    );
  }

  if (!story) {
    return (
      <div className="no-story">
        <h3>Story not found</h3>
        <p>The story you're looking for doesn't exist.</p>
      </div>
    );
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
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
    <div className="story-detail">
      <div className="story-header">
        <h1 className="story-title">{story.title}</h1>
        <div className="story-meta-large">
          <span className={`genre-badge genre-${story.genre}`}>
            {story.genre}
          </span>
          <span className="language-badge">
            {getLanguageName(story.language)}
          </span>
          <span className="length-badge">
            {story.length}
          </span>
          {story.tone && (
            <span className="tone-badge">
              {story.tone}
            </span>
          )}
        </div>
        
        <div className="story-info">
          <span className="word-count">{story.word_count} words</span>
          <span className="created-at">Created on {formatDate(story.created_at)}</span>
        </div>
      </div>

      {story.prompt && (
        <div className="story-prompt">
          <h3>Original Prompt</h3>
          <p>{story.prompt}</p>
        </div>
      )}

      <div className="story-content">
        <h3>Your Story</h3>
        <div className="content-text">
          {story.content.split('\n').map((paragraph, index) => (
            <p key={index}>{paragraph}</p>
          ))}
        </div>
      </div>

      {(story.characters && story.characters.length > 0) && (
        <div className="story-characters">
          <h3>Characters</h3>
          <div className="characters-list">
            {story.characters.map((character, index) => (
              <span key={index} className="character-tag">
                {character}
              </span>
            ))}
          </div>
        </div>
      )}

      {story.setting && (
        <div className="story-setting">
          <h3>Setting</h3>
          <p>{story.setting}</p>
        </div>
      )}
    </div>
  );
};

export default StoryDetail;