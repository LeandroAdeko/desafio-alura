import React, { useState, useEffect } from 'react';
import sendPing from '../../services/ping'

function Ping() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    sendPing.sendPing()
      .then(response => response.text())
      .then(data => setMessage(data));
  }, []);

  return (
    <div>
      <h1>React Frontend</h1>
      <p>Message from backend: '{message}'</p>
    </div>
  );
}

export default Ping;
