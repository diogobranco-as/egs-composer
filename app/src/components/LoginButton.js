import { useAuth0 } from "@auth0/auth0-react";
import '../styles/button.css'; 

const LoginButton = () => {
  const { loginWithRedirect, isAuthenticated } = useAuth0();

  const handleSignUp = async () => {
    try {
      // Redirect to Auth0 login
      await loginWithRedirect();
    } catch (error) {
      console.error('Failed to sign up:', error);
    }
  };

  return (
    !isAuthenticated && (
      <button onClick={() => handleSignUp()}>
        Sign In
      </button>
    )
  );
};

export default LoginButton;