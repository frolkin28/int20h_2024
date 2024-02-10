import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { SignUpForm } from "../../components"
import { AuthContext } from "../../AuthContext";
import {useEffect} from "react";

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
      <h1>Реєстрація</h1>
      <SignUpForm />
    </div>
  )
}