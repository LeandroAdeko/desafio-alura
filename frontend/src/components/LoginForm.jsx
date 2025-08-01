import React, { useState } from 'react';
import login from '../services/login';

const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await login(email, password);

      const data = await response.json();

      console.log(data);

      if (response.ok) {
        sessionStorage.setItem('accessToken', data.access_token);
        alert('Login successful!');
        // Redirect or update UI as needed
      } else {
        console.log(data);
        alert('Login failed: ' + data.message);
      }
    } catch (error) {
      alert('Login failed: ' + error.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className='label-input'>
        <label htmlFor="email">E-mail:</label>
        <input
          placeholder='exemplo@exemplo.com'
          type="text"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>
      <div className='label-input'>
        <label htmlFor="password" >Senha:</label>
        <input
          type="password"
          id="password"
          placeholder='******'
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
      <button type="submit">Login</button>
    </form>
  );
};

export default LoginForm;
