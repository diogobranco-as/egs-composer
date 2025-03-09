import LoginButton from "./components/LoginButton";
import LogoutButton from "./components/LogoutButton";
import './App.css';

function App() {
  return (
    <main>
      <h1>Auth0 Login</h1>
      <LoginButton />
      <LogoutButton />
    </main>
  );
}

export default App;