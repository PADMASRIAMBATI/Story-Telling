import React, { useState, useEffect } from 'react';
import { storiesAPI } from '../services/api';
import StoryList from '../components/Stories/StoryList';
import '../styles/Stories.css';

const StoryHistory = () => {
  const [stories, setStories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [pagination, setPagination] = useState({
    skip: 0,
    limit: 20,
    total: 0
  });

  const fetchStories = async () => {
    try {
      setLoading(true);
      const response = await storiesAPI.getAll(pagination.skip, pagination.limit);
      const data = response.data;
      setStories(data.stories);
      setPagination(prev => ({
        ...prev,
        total: data.total_count
      }));
    } catch (error) {
      console.error('Error fetching stories:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStories();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="story-history-page">
      <div className="page-header">
        <h1>My Stories</h1>
        <p>All your created stories in one place</p>
      </div>

      <div className="stories-container">
        <StoryList stories={stories} loading={loading} />
      </div>

      {!loading && stories.length > 0 && (
        <div className="pagination-info">
          <p>
            Showing {stories.length} of {pagination.total} stories
          </p>
        </div>
      )}
    </div>
  );
};

export default StoryHistory;