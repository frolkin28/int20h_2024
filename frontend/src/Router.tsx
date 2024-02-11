import React from "react";
import { createBrowserRouter } from "react-router-dom";
import { NavbarLayout } from "./layouts";
import {
  HomePage,
  LotPage,
  SignInPage,
  SignUpPage,
  AddLotPage,
  EditLotPage,
} from "./pages";

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
        element: <AddLotPage />,
      },
      {
        path: "/lots/:lotId",
        element: <LotPage />,
      },
      {
        path: "/lots/edit/:lotId",
        element: <EditLotPage />,
      },
    ],
  },
]);
