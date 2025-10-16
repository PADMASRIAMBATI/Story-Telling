import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { storiesAPI } from '../services/api';
import StoryForm from '../components/Stories/StoryForm';
import Modal from '../components/Common/Modal';
import '../styles/Stories.css';

const CreateStory = () => {
  const [loading, setLoading] = useState(false);
  const [generatedStory, setGeneratedStory] = useState(null);
  const [showSuccessModal, setShowSuccessModal] = useState(false);
  const navigate = useNavigate();

  const handleGenerateStory = async (storyData) => {
    setLoading(true);
    try {
      const response = await storiesAPI.generate(storyData);
      const story = response.data.story;
      setGeneratedStory(story);
      setShowSuccessModal(true);
    } catch (error) {
      console.error('Error generating story:', error);
      alert('Failed to generate story. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleViewStory = () => {
    setShowSuccessModal(false);
    navigate(`/story/${generatedStory.id}`);
  };

  const handleCreateAnother = () => {
    setShowSuccessModal(false);
    setGeneratedStory(null);
  };

  return (
    <div className="create-story-page">
      <div className="page-header">
        <h1>Create New Story</h1>
        <p>Fill in the details below and let AI work its magic!</p>
      </div>

      <div className="create-story-container">
        <StoryForm onSubmit={handleGenerateStory} loading={loading} />
      </div>

      <Modal
        isOpen={showSuccessModal}
        onClose={handleViewStory}
        title="🎉 Story Generated Successfully!"
      >
        <div className="success-modal-content">
          <p>Your story "{generatedStory?.title}" has been created successfully!</p>
          <div className="modal-actions">
            <button onClick={handleViewStory} className="btn btn-primary">
              Read Story
            </button>
            <button onClick={handleCreateAnother} className="btn btn-secondary">
              Create Another
            </button>
          </div>
        </div>
      </Modal>
    </div>
  );
};

export default CreateStory;