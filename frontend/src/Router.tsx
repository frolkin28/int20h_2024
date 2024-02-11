import React from "react";
import { createBrowserRouter } from 'react-router-dom';
import { NavbarLayout } from "./layouts";
import { HomePage, LotPage, SignInPage, SignUpPage } from "./pages";

export const router = createBrowserRouter([
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
        element: <SignInPage />,
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
