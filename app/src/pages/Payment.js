import React from 'react';
import { useParams } from 'react-router-dom';
import PaymentWidget from '../components/PaymentWidget';
import '../styles/payment.css'; 
const Payment = () => {
  const { productId } = useParams();
  return (
    <div className="Payment">
      <h1>Payment</h1>
      {productId && <PaymentWidget productId={productId} />}
    </div>
  );
};

export default Payment;