import React, { useState } from 'react';
import { GENRES, LANGUAGES, LENGTHS, TONES } from '../../utils/constants';
import Input from '../Common/Input';
import Button from '../Common/Button';
import '../../styles/Stories.css';

const StoryForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    prompt: '',
    genre: 'fantasy',
    language: 'en',
    length: 'medium',
    tone: 'light_hearted',
    characters: '',
    setting: ''
  });

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const submissionData = {
      ...formData,
      characters: formData.characters ? formData.characters.split(',').map(c => c.trim()) : [],
      setting: formData.setting || undefined
    };
    
    onSubmit(submissionData);
  };

  return (
    <form className="story-form" onSubmit={handleSubmit}>
      <div className="form-section">
        <h3>Story Basics</h3>
        
        <div className="input-group">
          <label className="input-label">Story Prompt *</label>
          <textarea
            value={formData.prompt}
            onChange={(e) => handleChange('prompt', e.target.value)}
            placeholder="Describe what you want your story to be about..."
            className="input-field textarea"
            rows="4"
            required
          />
        </div>

        <div className="form-row">
          <div className="input-group">
            <label className="input-label">Genre *</label>
            <select
              value={formData.genre}
              onChange={(e) => handleChange('genre', e.target.value)}
              className="input-field"
            >
              {GENRES.map(genre => (
                <option key={genre.value} value={genre.value}>
                  {genre.label}
                </option>
              ))}
            </select>
          </div>

          <div className="input-group">
            <label className="input-label">Language *</label>
            <select
              value={formData.language}
              onChange={(e) => handleChange('language', e.target.value)}
              className="input-field"
            >
              {LANGUAGES.map(lang => (
                <option key={lang.value} value={lang.value}>
                  {lang.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="input-group">
            <label className="input-label">Length *</label>
            <select
              value={formData.length}
              onChange={(e) => handleChange('length', e.target.value)}
              className="input-field"
            >
              {LENGTHS.map(length => (
                <option key={length.value} value={length.value}>
                  {length.label}
                </option>
              ))}
            </select>
          </div>

          <div className="input-group">
            <label className="input-label">Tone</label>
            <select
              value={formData.tone}
              onChange={(e) => handleChange('tone', e.target.value)}
              className="input-field"
            >
              {TONES.map(tone => (
                <option key={tone.value} value={tone.value}>
                  {tone.label}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      <div className="form-section">
        <h3>Additional Details (Optional)</h3>
        
        <Input
          label="Characters (comma-separated)"
          value={formData.characters}
          onChange={(e) => handleChange('characters', e.target.value)}
          placeholder="e.g., Brave knight, Wise wizard, Funny sidekick"
        />

        <Input
          label="Setting"
          value={formData.setting}
          onChange={(e) => handleChange('setting', e.target.value)}
          placeholder="e.g., Ancient forest, Space station, Magical kingdom"
        />
      </div>

      <Button 
        type="submit" 
        variant="primary" 
        loading={loading}
        className="generate-btn"
      >
        🪄 Generate Story
      </Button>
    </form>
  );
};

export default StoryForm;