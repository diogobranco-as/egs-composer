import React, { useState, useEffect } from "react";

const API_BASE_URL = "http://127.0.0.1:8001/v1";

function ReviewWidget({ productId }) {
  const [reviews, setReviews] = useState([]);
  const [review, setReview] = useState({ rating: "", comment: "" });
  const [editReview, setEditReview] = useState(null);

  useEffect(() => {
    if (productId) {
      fetch(`${API_BASE_URL}/entities/${productId}/reviews`)
        .then((res) => res.json())
        .then((data) => setReviews(data))
        .catch(() => setReviews([]));
    }
  }, [productId]);

  const handleReviewSubmit = (e) => {
    e.preventDefault();
    fetch(`${API_BASE_URL}/reviews`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        entity_id: productId,
        rating: parseFloat(review.rating),
        comment: review.comment,
      }),
    })
      .then((res) => res.json())
      .then(() => {
        alert("Review submitted!");
        setReview({ rating: "", comment: "" });
        fetchReviews(); // Refresh reviews
      })
      .catch((err) => console.error("Error submitting review:", err));
  };

  const fetchReviews = () => {
    fetch(`${API_BASE_URL}/entities/${productId}/reviews`)
      .then((res) => res.json())
      .then((data) => setReviews(data))
      .catch(() => setReviews([]));
  };

  const handleReviewDelete = (reviewId) => {
    fetch(`${API_BASE_URL}/entities/${productId}/reviews/${reviewId}`, {
      method: "DELETE",
    })
      .then(() => {
        alert("Review deleted!");
        fetchReviews();
      })
      .catch((err) => console.error("Error deleting review:", err));
  };

  return (
    <div style={{ border: "1px solid #ddd", padding: "10px", margin: "10px", width: "300px" }}>
      <h3>Reviews</h3>
      <ul>
        {reviews.length > 0 ? (
          reviews.map((rev) => (
            <li key={rev.id}>
              <strong>{rev.rating}/5</strong> - {rev.comment}
              <button onClick={() => handleReviewDelete(rev.id)}>Delete</button>
            </li>
          ))
        ) : (
          <p>No reviews yet.</p>
        )}
      </ul>

      <h4>Submit a Review</h4>
      <form onSubmit={handleReviewSubmit}>
        <label>Rating (1-5): </label>
        <input
          type="number"
          min="1"
          max="5"
          value={review.rating}
          onChange={(e) => setReview({ ...review, rating: e.target.value })}
          required
        />
        <br />
        <label>Comment: </label>
        <input
          type="text"
          value={review.comment}
          onChange={(e) => setReview({ ...review, comment: e.target.value })}
        />
        <br />
        <button type="submit">Submit Review</button>
      </form>
    </div>
  );
}

export default ReviewWidget;