import { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../AuthContext";
import { SignInForm } from "../../components";
import styles from "./SingIn.module.css";

export const SignInPage = () => {
  const navigate = useNavigate();
  const { isSignedIn } = useContext(AuthContext)

  useEffect(() => {
    if (isSignedIn) {
      navigate("/")
    }
  }, [isSignedIn])

  return (
    <div>
      <h1 className={styles["title"]}>Вхід</h1>
      <SignInForm />
    </div>
  )
}
