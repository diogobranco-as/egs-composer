import React from 'react';
import { useNavigate } from 'react-router-dom';

const ProductBox = ({ product }) => {
  const navigate = useNavigate();

  const handleReviewClick = () => {
    navigate(`/products/${product.product_id}/reviews`);
  };

  const handleBuyClick = () => {
    navigate(`/payment`);
  }

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