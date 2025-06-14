import React from 'react';

const PurchasedGame = ({ item }) => {
console.log(item);
  return (
    <div className="purchased-item">
      <h2>{item.product_name}</h2>
    </div>
  );
};

export default PurchasedGame;