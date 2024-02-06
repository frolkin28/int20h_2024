import React from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { HomePage, LotPage } from "./pages"
import './App.css';

const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
    errorElement: <h1>Page not found</h1>
  },
  {
    path: "/lots/:lotId",
    element: <LotPage />
  }
]);

const App = () => {
  return (
    <RouterProvider router={router} />
  )
}

export default App;
