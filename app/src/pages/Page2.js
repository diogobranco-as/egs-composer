import React, { useState, useEffect } from 'react';
import '../styles/page2.css';

const Page2 = () => {
  const [nickname, setNickname] = useState(null);

  useEffect(() => {
    const storedNickname = localStorage.getItem('chatNickname');
    if (storedNickname) {
      setNickname(storedNickname);
    } else {
      setNickname('guest');
    }
  }, []);

  if (!nickname) return <p>Loading chat...</p>;

  return (
    <div className="page2" style={{ width: '100%', height: '100vh' }}>
      <iframe 
        src={`http://localhost:8080?nickname=${encodeURIComponent(nickname)}`} 
        style={{ width: '100%', height: '100%', border: 'none' }}
        title="Chat Interface"
      />
    </div>
  );
};

export default Page2;
