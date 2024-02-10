import React from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { AuthContext } from "./AuthContext";
import { useAuth } from "./hooks";
import { NavbarLayout } from "./layouts";
import { HomePage, LotPage, SignUpPage } from "./pages"
import './App.css';

const router = createBrowserRouter([
  {
    path: "/",
    element: <NavbarLayout />,
    errorElement: <h1>Сторінка не знайдена</h1>,
    children: [
      {
        path: "/",
        element: <HomePage />,
      },
      {
        path: "/sign-in",
        element: <h1>Sign In</h1>,
      },
      {
        path: "/sign-up",
        element: <SignUpPage />,
      },
      {
        path: "/add-lot",
        element: <h1>Add lot</h1>
      },
      {
        path: "/lots/:lotId",
        element: <LotPage />
      }
    ]
  },
]);

const App = () => {
  const { isSignedIn, login, logout } = useAuth()

  return (
    <AuthContext.Provider value={{ isSignedIn, login, logout }}>
      <RouterProvider router={router} />
    </AuthContext.Provider>
  )
}

export default App;
