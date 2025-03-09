import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';

const Profile = () => {
  const { user } = useAuth0();

  return (
    <div>
      <h1>Profile</h1>
      {user && (
        <div>
          <img src={user.picture} alt={user.name} />
          <h2>{user.name}</h2>
          <ul>
            {Object.keys(user).map((key, i) => (
              <li key={i}>
                <strong>{key}:</strong> {user[key]}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default Profile;