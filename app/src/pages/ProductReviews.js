import React from 'react';
import { useParams } from 'react-router-dom';
import ReviewWidget from '../components/ReviewWidget';

const ProductReviews = () => {
  const { productId } = useParams();

  return (
    <div className="product-reviews-page">
      <h2>Product Reviews</h2>
      {productId && <ReviewWidget productId={productId} />}
    </div>
  );
};

export default ProductReviews;