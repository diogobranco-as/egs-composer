import React, { useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import '../styles/home.css';

const Home = () => {
  const { user, isAuthenticated } = useAuth0();

  useEffect(() => {
    if (isAuthenticated && user) {
      localStorage.setItem('chatNickname', user.nickname || user.name);
    }
  }, [isAuthenticated, user]);

  return (
    <div className="home">
      <h1>Welcome to PlayerXpress</h1>
      <p>Home of the best game deals</p>
    </div>
  );
};

export default Home;