import { createContext } from "react";

interface AuthContext {
  isSignedIn: boolean;
  login: (token: string) => void;
  logout: () => void;
  token: string | null;
}

export const AuthContext = createContext<AuthContext>({
  isSignedIn: false,
  login: () => {},
  logout: () => {},
  token: null,
});
