import React, { useEffect, useState, useRef, useCallback } from 'react';
import ProductBox from '../components/ProductBox';
import '../styles/products.css';
import { useAuth0 } from '@auth0/auth0-react';
import { useNavigate, useSearchParams } from 'react-router-dom';

const Products = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [offset, setOffset] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const { user } = useAuth0();
  const [searchParams] = useSearchParams();
  const paymentId = searchParams.get('paymentId');
  const productId = searchParams.get('productId');
  const hasProcessedPurchase = useRef(false);
  const navigate = useNavigate();


  const limit = 10; // increase later (20? 40?)
  const hasFetched = useRef(false);
  const createPurchasedRecord = useCallback(async () => {
    console.log('Creating purchased record...');
    console.log('hello mfer');
    console.log('API URL:', process.env.REACT_APP_API_URL);

    if (!paymentId || !productId || !user?.sub || hasProcessedPurchase.current) return;
  
    try {

      const auth0_id = encodeURIComponent(user.sub);
      const response = await fetch(`${process.env.REACT_APP_API_URL}/v1/purchased/${auth0_id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          payment_id: paymentId,
          product_id: productId,
          user_id: user.sub, 
        }),
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create purchased record');
      }
  
      const result = await response.json();
      console.log('Purchase recorded:', result);
      hasProcessedPurchase.current = true;
  
      // Clean up URL params
      searchParams.delete('paymentId');
      searchParams.delete('productId');
      navigate({ search: searchParams.toString() }, { replace: true });
      
    } catch (error) {
      console.error('Error creating purchased record:', error.message);
    }
  }, [paymentId, productId, user?.sub, searchParams, navigate]);
  
  const fetchProducts = useCallback(async () => {
    if (hasFetched.current) return; 
    hasFetched.current = true;

    setLoading(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_API_URL}/v1/products/?limit=${limit}&offset=${offset}`);
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
    createPurchasedRecord();
  }, [fetchProducts, createPurchasedRecord]); 

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