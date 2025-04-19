import React from "react";

const TikTokAuthButton = () => {
  const redirectToTikTok = () => {
    const clientKey = process.env.REACT_APP_TIKTOK_CLIENT_KEY;
    const redirectUri = encodeURIComponent("https://yourdomain.com/tiktok/callback/"); // Replace with your actual URL or ngrok link
    const scope = "user.info.basic video.upload video.publish";

    window.location.href = `https://www.tiktok.com/v2/auth/authorize?client_key=${clientKey}&response_type=code&scope=${scope}&redirect_uri=${redirectUri}`;
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gery-100">
      <button
        onClick={redirectToTikTok}
        className="btn btn-danger px-4 py-2 text-white rounded shadow-sm"
      >
        Connect with TikTok
      </button>
    </div>
  );
};

export default TikTokAuthButton;
