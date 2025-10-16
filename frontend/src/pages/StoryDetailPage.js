import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { storiesAPI } from '../services/api';
import StoryDetail from '../components/Stories/StoryDetail';
import LoadingSpinner from '../components/Layout/LoadingSpinner';
import '../styles/Stories.css';

const StoryDetailPage = () => {
  const { id } = useParams();
  const [story, setStory] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchStory = async () => {
      try {
        setLoading(true);
        const response = await storiesAPI.getById(id);
        setStory(response.data.story);
      } catch (err) {
        setError('Failed to load story');
        console.error('Error fetching story:', err);
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchStory();
    }
  }, [id]);

  if (loading) {
    return (
      <div className="story-detail-page">
        <LoadingSpinner text="Loading story..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="story-detail-page">
        <div className="error-state">
          <h3>Error</h3>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="story-detail-page">
      <StoryDetail story={story} loading={false} />
    </div>
  );
};

export default StoryDetailPage;