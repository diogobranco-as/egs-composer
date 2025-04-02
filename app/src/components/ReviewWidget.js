import React, { useEffect } from "react";

const ReviewWidget = ({ productId }) => {
  useEffect(() => {
    
    const handleLoad = () => {
      if (window.loadReviews) {
        window.loadReviews(productId, 'review-container');
      }
    };

    if (window.loadReviews) {
      handleLoad();
      return;
    }

    const script = document.createElement('script');
    script.src = "http://127.0.0.1:8001/static/review-widget.js";
    script.async = true;
    script.onload = handleLoad;
    
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, [productId]);

  return (
    <div id="review-container" style={{ margin: '20px 0', border: '1px solid red' }}>
      {/* Temporary border to verify container exists */}
      Loading reviews...
    </div>
  );
};

export default ReviewWidget;