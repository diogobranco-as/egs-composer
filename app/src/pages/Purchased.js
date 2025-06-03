import React, { useEffect, useState, useCallback } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import PurchasedGame from '../components/PurchasedGame';
import '../styles/purchased.css';

const Purchased = () => {
  const { user } = useAuth0();
  const userId = user?.sub

  const [purchasedItems, setPurchasedItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchPurchased = useCallback(async () => {
    if (!userId) return;
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/v1/purchased/${userId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch purchased items');
      }
      const data = await response.json();
      setPurchasedItems(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    if (userId) {
      fetchPurchased();
    }
  }, [userId, fetchPurchased]);

  return (
    <div className="purchased">
      <h1>My Purchased Games</h1>
      {loading && <div className="loading">Loading...</div>}
      {error && <div className="error">Error: {error}</div>}
      {!loading && !error && purchasedItems.length === 0 && (
        <div className="no-items">No purchased games found.</div>
      )}
      <div className="purchased-games-list">
        {purchasedItems.map((item) => (
          <PurchasedGame key={item.payment_id} item={item} />
        ))}
      </div>
    </div>
  );
};

export default Purchased;