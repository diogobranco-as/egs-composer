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
      <h1>Welcome to the Home Page</h1>
      <p>This is the home page of the application.</p>
    </div>
  );
};

export default Home;