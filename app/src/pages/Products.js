import React, { useEffect, useState, useRef, useCallback } from 'react';
import ProductBox from '../components/ProductBox';
import '../styles/products.css';

const Products = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [offset, setOffset] = useState(0);
  const [hasMore, setHasMore] = useState(true);

  const limit = 10; // increase later (20? 40?)
  const hasFetched = useRef(false);

  const fetchProducts = useCallback(async () => {
    if (hasFetched.current) return; 
    hasFetched.current = true;

    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/v1/products/?limit=${limit}&offset=${offset}`);
      if (!response.ok) {
        throw new Error('Failed to fetch products');
      }
      const data = await response.json();
      if (data.length === 0) {
        setHasMore(false); // No more products to load
      } else {
        setProducts((prevProducts) => [...prevProducts, ...data]); // Append new products
        setOffset((prevOffset) => prevOffset + limit); // Update offset
      }
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  }, [limit, offset]); 
  
  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]); 

  // Reset hasFetched when the "Load More" button is clicked
  const handleLoadMore = () => {
    hasFetched.current = false;
    fetchProducts();
  };

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div className="products">
      <h1>Products</h1>
      <div className="product-grid">
        {products.map((product) => (
          <ProductBox key={product.product_id} product={product} />
        ))}
      </div>
      {loading && <div>Loading...</div>}
      {hasMore && !loading && (
        <div className="load-more-container">
          <button onClick={handleLoadMore} className="load-more-button">
            Load More
          </button>
        </div>
      )}
      {!hasMore && <div>No more products to load.</div>}
    </div>
  );
};

export default Products;