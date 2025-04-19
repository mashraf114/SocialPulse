import React from 'react';

const TikTokAuthButton = () => {
  const handleTikTokAuth = async () => {
    try {
      // Step 1: Call your Django backend to get the TikTok auth URL
      const response = await fetch(`${process.env.REACT_APP_API_BASE_URL}/tiktok/auth/`);
      
      if (!response.ok) {
        throw new Error('Failed to get auth URL');
      }
      
      const data = await response.json();
      
      // Step 2: Redirect to TikTok's auth page
      window.location.href = data.auth_url;
      
    } catch (error) {
      console.error('Authentication error:', error);
      // Handle error in your UI
    }
  };

  return (
    <button onClick={handleTikTokAuth}>
      Connect TikTok Account
    </button>
  );
};

export default TikTokAuthButton;