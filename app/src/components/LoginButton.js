import { useAuth0 } from "@auth0/auth0-react";
import '../styles/button.css'; 

const LoginButton = () => {
  const { loginWithRedirect, isAuthenticated, user } = useAuth0();

  const handleSignUp = async () => {
    await loginWithRedirect();
    if (user){
      //send user to backend
      const userData = { //Auth0 user data
        user_id: user.sub,
        email: user.email,
        name: user.name || user.email,
      };

      try{
        const response = await fetch('http://localhost:5000/auth/signup', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(userData),
        });

        if (!response.ok){
          throw new Error('Failed to create user');
        }

        const result = await response.json();
        console.log("User created", result);
      } catch (error){
        console.error('Failed to create user', error);
      }
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