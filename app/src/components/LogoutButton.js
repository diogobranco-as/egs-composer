import { useAuth0 } from "@auth0/auth0-react";
import '../styles/button.css'; 

const LogoutButton = () => {
  const { logout, isAuthenticated } = useAuth0();

  return (
    isAuthenticated && (
      <button className="logout" onClick={() => logout()}>
        Sign Out
      </button>
    )
  );
};

export default LogoutButton;