import React from 'react';
import { Outlet } from 'react-router-dom';
import { Navbar } from '../../components';
import styles from "./NavbarLayout.module.css"

export const NavbarLayout = () => {
  return (
    <div>
      <Navbar />
      <div className={styles.container}>
        <Outlet />
      </div>
    </div>
  )
}