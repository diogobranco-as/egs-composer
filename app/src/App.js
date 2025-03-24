import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Products from './pages/Products';
import ProductReviews from './pages/ProductReviews';
import Page2 from './pages/Page2';
import Profile from './components/Profile';
import './styles/global.css';
import './styles/app.css';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/products" element={<Products />} />
        <Route path="/products/:productId/reviews" element={<ProductReviews />} />
        <Route path="/page2" element={<Page2 />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </Router>
  );
}

export default App;