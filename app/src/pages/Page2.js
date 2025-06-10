import React, { useState, useEffect } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import '../styles/page2.css';

const Page2 = () => {
  const [nickname, setNickname] = useState(null);
  const { isAuthenticated } = useAuth0();

  useEffect(() => {
    if (!isAuthenticated) return;
    
    const storedNickname = localStorage.getItem('chatNickname');
    if (storedNickname) {
      setNickname(storedNickname);
    } else {
      setNickname('guest');
    }
  }, [isAuthenticated]);

  if (!isAuthenticated) {
    return (
      <div className="page2" style={{ width: '100%', height: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <div className="auth-message">
          Please sign in to access the chat.
        </div>
      </div>
    );
  }

  if (!nickname) return <p>Loading chat...</p>;

  return (
    <div className="page2" style={{ width: '100%', height: '100vh' }}>
      <iframe 
        src={`${process.env.REACT_APP_CHATSERVICE_URL}?nickname=${encodeURIComponent(nickname)}`} 
        style={{ width: '100%', height: '100%', border: 'none' }}
        title="Chat Interface"
      />
    </div>
  );
};

export default Page2;
