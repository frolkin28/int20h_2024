import { useState, useEffect } from "react";

const ACCESS_TOKEN_KEY = "access_token"

export const useAuth = () => {
  const [isSignedIn, setSignedIn] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem(ACCESS_TOKEN_KEY)
    setSignedIn(!!token)
  }, [])

  const login = (token: string) => {
    localStorage.setItem(ACCESS_TOKEN_KEY, token)
    setSignedIn(true)
  }

  const logout = () => {
    localStorage.removeItem(ACCESS_TOKEN_KEY)
    setSignedIn(false)
  }

  return { isSignedIn, login, logout}
}
