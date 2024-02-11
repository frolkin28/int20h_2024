import React, { useContext } from 'react';
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../../AuthContext";
import styles from './Navbar.module.css';

export const Navbar = () => {
  const navigate = useNavigate();

  const { isSignedIn, logout } = useContext(AuthContext);

  const handleLogout = () => {
    logout()
    navigate("/")
  }

  const renderLinks = () => {
    if (isSignedIn) {
      return (
        <li>
          <button onClick={handleLogout}>Вийти</ button>
        </li>
      )
    }
    return (
      <>
        <li>
          <Link to="sign-in" >Вхід</Link>
        </li>
        <li>
          <Link to="sign-up" >Реєстрація</Link>
        </li>
      </>
    )
  }

  return (
    <div className={styles.container}>
      <Link to="/" className={styles["link-logo"] }>
        <p className={styles["logo"]}>charity auction</p>
        <img src="https://dq5d23gxa9vto.cloudfront.net/logo.png" width={"30px"} alt="LOGO" />
      </Link>
      <ul className={styles['buttons-list']}>
        <li>
          <Link className={styles["add-lot"]} to={isSignedIn ? "/add-lot" : "/sign-in"} >Додати</Link>
        </li>
        {renderLinks()}
      </ul>
    </div>
  )
}
