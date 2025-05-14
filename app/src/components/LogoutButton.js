import { useAuth0 } from "@auth0/auth0-react";
import '../styles/button.css'; 

const LogoutButton = () => {
  const { logout, isAuthenticated } = useAuth0();

  const handleLogout = () => {
    localStorage.removeItem("chatNickname");
    logout();
  }

  return (
    isAuthenticated && (
      <button className="logout" onClick={handleLogout}>
        Sign Out
      </button>
    )
  );
};

export default LogoutButton;