import { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { SignUpForm } from "../../components"
import { AuthContext } from "../../AuthContext";
import styles from "./SignUp.module.css";

export const SignUpPage = () => {
  const navigate = useNavigate();
  const { isSignedIn } = useContext(AuthContext)

  useEffect(() => {
    if (isSignedIn) {
      navigate("/")
    }
  }, [isSignedIn])

  return (
    <div>
      <h1 className={styles["title"]}>Реєстрація</h1>
      <SignUpForm />
    </div>
  )
}