import { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';
import TikTokAuthButton from './components/TikTokAuthButton';
import TikTokUploader from './components/TikTokUploader';

import TikTokSuccessPage from './pages/TikTokSuccessPage.jsx';

function App() {
  const [msg, setMsg] = useState("");
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    fetch("http://127.0.0.1:3333/ping/")
      .then(res => res.json())
      .then(data => setMsg(data.message))
      .catch(err => console.error("Error fetching ping:", err));
  }, []);

  return (
    <Router>
      <div className="App">
        <header>
          <h1>TikTok Integration</h1>
          <p>Server status: {msg}</p>
        </header>

        <main>
          <Routes>
            {/* Main page with auth/upload components */}
            <Route path="/" element={
              <>
                {!isAuthenticated && <TikTokAuthButton onSuccess={() => setIsAuthenticated(true)} />}
                {isAuthenticated && <TikTokUploader />}
              </>
            } />
            
            {/* Success callback route */}
            <Route path="/tiktok-success" element={
              <TikTokSuccessPage 
                onSuccess={() => setIsAuthenticated(true)}
              />
            } />
            
          </Routes>
        </main>
      </div>
    </Router>
    
  );
}

export default App;