import { useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';

const TikTokSuccessPage = ({ onSuccess }) => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  useEffect(() => {
    const success = searchParams.get('success');
    const error = searchParams.get('error');
    const code = searchParams.get('code');
    
    if (code) {
      // Send code to backend for token exchange
      fetch('/api/tiktok/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
      })
        .then(res => res.json())
        .then(data => {
          onSuccess?.(data);
          navigate('/dashboard');
        })
        .catch(err => {
          console.error('Token exchange failed:', err);
          navigate('/?error=auth_failed');
        });
    }
    else if (error) {
      navigate(`/?error=${error}`);
    }
  }, [searchParams, navigate, onSuccess]);

  return (
    <div className="flex justify-center items-center h-screen">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-tiktok-pink mx-auto mb-4"></div>
        <p className="text-lg">Connecting to TikTok...</p>
      </div>
    </div>
  );
};

TikTokSuccessPage.propTypes = {
  onSuccess: PropTypes.func
};

export default TikTokSuccessPage;