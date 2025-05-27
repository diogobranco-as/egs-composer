import React from 'react';
import { useNavigate } from 'react-router-dom';

const ProductBox = ({ product }) => {
  const navigate = useNavigate();

  const handleReviewClick = () => {
    navigate(`/products/${product.product_id}/reviews`);
  };

  const handleBuyClick = async () => {    
    try {
      const paymentData = {
        amount: product.product_price,
        currency: 'EUR',
        product_id: product.product_id
      };
      window.location.href = `http://localhost:5173?amount=${paymentData.amount}&currency=${paymentData.currency}&product_id=${paymentData.product_id}`;      
    } catch (error) {
      console.error('6. Payment error:', error.message);
      if (error.name === 'TypeError') {
        console.error('7. Network error details:', error);
      }
    }
  };

  return (
    <div className="product-box">
      <h2>{product.product_name}</h2>
      <p><strong>Type:</strong> {product.product_type}</p>
      <p><strong>Price:</strong> ${product.product_price}</p>
      <p><strong>Provider:</strong> {product.product_seller}</p>
      <div className="product-actions">
        <button className="reviews-button" onClick={handleReviewClick}>Reviews</button>
        <button className="buy-button" onClick={handleBuyClick}>Buy</button>
      </div>
    </div>
  );
};

export default ProductBox;