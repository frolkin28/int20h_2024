import React, {useContext, useState} from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { TextInput, Button } from "../";
import { AuthContext } from "../../AuthContext";
import styles from './SingInForm.module.css';

export const SignInForm = () => {
  const navigate = useNavigate();
  const { login } = useContext(AuthContext);

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSubmitting, setSubmitting] = useState(false)

  const handleEmailChange = (value: string) => setEmail(value)
  const handlePasswordChange = (value: string) => setPassword(value)

  const handleSubmit = async () => {
    setSubmitting(true)
    try {
      if (!email.length) {
        return alert("Введіть email")
      }
      if (!password.length) {
        return alert("Введіть пароль")
      }

      const res = await axios.post(`${process.env.REACT_APP_BASE_URL}/api/auth/sign_in`, {
        email,
        password,
      })
      login(res.data.data.access_token)
      navigate("/")
    } catch (error: any) {
      const message = error.response.status === 400 ? "Неправильні дані для входу" : "Сталася помилка"
      alert(message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form className={styles["form-container"]}>
      <div>
        <label className={styles["form-label"]} htmlFor="email">Email</label>
        <TextInput id="email" value={email} onChange={handleEmailChange} />
      </div>
      <div>
        <label className={styles["form-label"]}  htmlFor="password">Пароль</label>
        <TextInput id="password" type="password" value={password} onChange={handlePasswordChange} />
      </div>
      <Button text="Авторизуватись" onClick={handleSubmit} disabled={isSubmitting} />
    </form>
  )
}
