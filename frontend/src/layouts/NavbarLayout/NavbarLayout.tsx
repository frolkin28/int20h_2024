import React from 'react';
import { Outlet } from 'react-router-dom';
import { Navbar } from '../../components';

export const NavbarLayout = () => {
  return (
    <div>
      <Navbar />
      <Outlet />
    </div>
  )
}