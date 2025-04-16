import { useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [msg, setMsg] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:3333/ping/")
      .then(res => res.json())
      .then(data => setMsg(data.message))
      .catch(err => console.error("Error fetching ping:", err));
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <p style={{ color: '#61dafb' }}>
          Django says: <strong>{msg || 'Loading...'}</strong>
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
