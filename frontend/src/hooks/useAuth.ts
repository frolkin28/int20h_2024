import { useState, useEffect } from "react";

export const useAuth = () => {
  const [isSignedIn, setSignedIn] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem("access_token")
    setSignedIn(!!token)
  }, [])

  const login = (token: string) => {
    localStorage.setItem("access_token", token)
    setSignedIn(true)
  }

  const logout = () => {
    localStorage.removeItem("access_token")
    setSignedIn(false)
  }

  return { isSignedIn, login, logout}
}
