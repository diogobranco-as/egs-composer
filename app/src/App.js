import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Auth0Provider, useAuth0 } from '@auth0/auth0-react';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Products from './pages/Products';
import ProductReviews from './pages/ProductReviews';
import Page2 from './pages/Page2';
import Profile from './components/Profile';
import Purchased from './pages/Purchased';
import './styles/global.css';
import './styles/app.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function AppWrapper() {
  return (
    <Auth0Provider
      domain="dev-ax53r2dultf84l0z.eu.auth0.com"
      clientId="813mXBOU53qMhXEd80gZKuKrfh5c3ec7"
      authorizationParams={{
        redirect_uri: window.location.origin,
        audience: 'https://playerxpress-api.com',
        scope: 'openid profile email',
      }}
      cacheLocation="localstorage"
    >
      <App />
    </Auth0Provider>
  );
}

function App() {
  const { isAuthenticated, user, getAccessTokenSilently } = useAuth0();
  const [internalUserId, setInternalUserId] = useState(
    localStorage.getItem('internal_user_id')
  );
  useEffect(() => {
    if (!isAuthenticated || !user) return;
    (async () => {
      try {
        const token = await getAccessTokenSilently({
          audience: 'https://playerxpress-api.com',
          scope: 'openid profile email',
        });

        const res = await fetch(`${API_URL}/v1/users/sync`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
          auth0_id: user.sub,
          user_email: user.email,
          user_name: user.nickname || user.email.split('@')[0],
          email_verified: user.email_verified
        }),
        });
        const data = await res.json();
        if (data.user_id) {
          setInternalUserId(data.user_id);
          localStorage.setItem('internal_user_id', data.user_id);
        }
      } catch (err) {
        console.error('Failed to sync user:', err);
      }
    })();
  }, [isAuthenticated, user, getAccessTokenSilently, internalUserId]);

  return (
    <Router>
      <Navbar internalUserId={internalUserId} />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/products" element={<Products />} />
        <Route path="/products/:productId/reviews" element={<ProductReviews />} />
        <Route path="/page2" element={<Page2 />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/purchased" element={<Purchased userId={internalUserId} />} />
      </Routes>
    </Router>
  );
}

export default AppWrapper;
