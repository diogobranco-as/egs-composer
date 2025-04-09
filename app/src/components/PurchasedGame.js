import React from 'react';

const PurchasedGame = ({ item }) => {

  return (
    <div className="purchased-item">
      <h2>{item.product_name}</h2>
      <p className="payment-id">Payment ID: {item.payment_id}</p>
    </div>
  );
};

export default PurchasedGame;