import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/Login.scss';
import { login } from '../services/api';
import { AuthContext } from '../App';

const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { setAuthenticated } = useContext(AuthContext);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      await login(username, password);
      setAuthenticated(true);
      navigate('/');
    } catch (err) {
      setError('Invalid username or password');
    }
  };

  return (
    <div className="login">
      <div className="login__container">
        <div className="login__box">
          <div className="login__logo">
            <img src="/logo512.png" alt="Prohelion Logo" />
          </div>
          <form className="login__form" onSubmit={handleSubmit}>
            <input
              type="text"
              className="login__input"
              placeholder="Username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
            <input
              type="password"
              className="login__input"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button type="submit" className="login__button">
              Sign In
            </button>
            {error && <div className="login__error">{error}</div>}
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login; 