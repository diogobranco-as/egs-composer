import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth0 } from '@auth0/auth0-react';
import LoginButton from './LoginButton';
import LogoutButton from './LogoutButton';
import '../styles/navbar.css'; 

const Navbar = () => {
  const { isAuthenticated, user } = useAuth0();

  return (
    <nav className="navbar">
      <ul className="navList">
        <li className="navItem">
          <Link to="/" className="navLink">Home</Link>
        </li>
        <li className="navItem">
          <Link to="/page1" className="navLink">Page 1</Link>
        </li>
        <li className="navItem">
          <Link to="/page2" className="navLink">Page 2</Link>
        </li>
      </ul>
      <div className="authSection">
        {!isAuthenticated ? (
          <LoginButton />
        ) : (
          <div className="dropdown">
            <button className="dropdownButton">
              {user?.name} <span>&#9660;</span>
            </button>
            <div className="dropdownContent">
              <Link to="/profile" className="dropdownLink">Profile</Link>
              <LogoutButton />
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;