import React, { useContext, useState } from 'react';
import axios from "axios"
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../AuthContext";
import { TextInput, Checkbox, Button } from "../";
import styles from './SignUpForm.module.css';

export const SignUpForm = () => {
  const navigate = useNavigate();
  const { login } = useContext(AuthContext);

  const [email, setEmail] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastname] = useState('');
  const [password, setPassword] = useState('');
  const [passwordRepeat, setPasswordRepeat] = useState('');
  const [isAgreed, setAgreed] = useState(false)
  const [isSubmitting, setSubmitting] = useState(false)

  const handleEmailChange = (value: string) => setEmail(value)
  const handleFirstNameChange = (value: string) => setFirstName(value)
  const handleLastNameChange = (value: string) => setLastname(value)
  const handlePasswordChange = (value: string) => setPassword(value)
  const handlePasswordRepeatChange = (value: string) => setPasswordRepeat(value)
  const handleAgreedChange = () => setAgreed(prevState => !prevState)

  const handleSubmit = async () => {
    setSubmitting(true)
    if (!email.length) {
      return alert("Введіть email")
    }
    if (!firstName.length) {
      return alert("Введіть імʼя")
    }
    if (!lastName.length) {
      return alert("Введіть прізвище")
    }
    if (!password.length) {
      return alert("Введіть пароль")
    }
    if (password !== passwordRepeat) {
      return alert("Паролі не співпадають")
    }
    try {
      const res = await axios.post(`${process.env.REACT_APP_BASE_URL}/api/auth/sign_up`, {
        first_name: firstName,
        last_name: lastName,
        email: email,
        password: password
      })
      login(res.data.data.access_token)
      navigate("/")
    } catch (error) {
      alert("Сталася помилка")
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form className={styles["form-container"]}>
      <div >
        <label className={styles["form-label"]} htmlFor="email">Email</label>
        <TextInput id="email" value={email} onChange={handleEmailChange} />
      </div>
      <div>
        <label className={styles["form-label"]} htmlFor="first-name">Імʼя</label>
        <TextInput id="first-name" value={firstName} onChange={handleFirstNameChange} />
      </div>
      <div>
        <label className={styles["form-label"]} htmlFor="last-name">Прізвище</label>
        <TextInput id="last-name" value={lastName} onChange={handleLastNameChange} />
      </div>
      <div>
        <label className={styles["form-label"]} htmlFor="password">Пароль</label>
        <TextInput id="password" type="password" value={password} onChange={handlePasswordChange} />
      </div>
      <div>
        <label className={styles["form-label"]} htmlFor="password-repeat">Повторіть пароль</label>
        <TextInput id="password-repeat" type="password" value={passwordRepeat} onChange={handlePasswordRepeatChange} />
      </div>
      <div>
        <Checkbox id="terms-and-conditions" checked={isAgreed} onChange={handleAgreedChange} />
        <label htmlFor="terms-and-conditions">Я підтверджую свою згоду з угодою користувача і погоджуюся з передачею та обробкою моїх персональних даних</label>
      </div>
      <Button text="Зареєструватися" onClick={handleSubmit} disabled={!isAgreed || isSubmitting} />
    </form>
  )
}
