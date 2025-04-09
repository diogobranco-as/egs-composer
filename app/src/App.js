import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Auth0Provider } from '@auth0/auth0-react';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Products from './pages/Products';
import ProductReviews from './pages/ProductReviews';
import Page2 from './pages/Page2';
import Profile from './components/Profile';
import Purchased from './pages/Purchased';
import './styles/global.css';
import './styles/app.css';

function App() {
  return (
    <Auth0Provider
      domain="dev-ax53r2dultf84l0z.eu.auth0.com"
      clientId="813mXBOU53qMhXEd80gZKuKrfh5c3ec7"
      authorizationParams={{
        redirect_uri: window.location.origin,
        audience: "https://playerxpress-api.com",
        scope: "openid profile email"
      }}
      cacheLocation="localstorage"
    >
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/products" element={<Products />} />
        <Route path="/products/:productId/reviews" element={<ProductReviews />} />
        <Route path="/page2" element={<Page2 />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/purchased" element={<Purchased />} />
      </Routes>
    </Router>
    </Auth0Provider>
  );
}

export default App;