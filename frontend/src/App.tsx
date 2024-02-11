import { RouterProvider } from "react-router-dom";
import { router } from "./Router";
import { AuthContext } from "./AuthContext";
import { useAuth } from "./hooks";
import "./App.css";

const App = () => {
  const { isSignedIn, login, logout } = useAuth();

  return (
    <AuthContext.Provider value={{ isSignedIn, login, logout }}>
      <RouterProvider router={router} />
    </AuthContext.Provider>
  );
};

export default App;
