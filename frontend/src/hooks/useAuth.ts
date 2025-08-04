import { useState, useEffect } from "react";

const TOKEN_KEY = "TOKEN_KEY";

export const useAuth = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(() => !!localStorage.getItem(TOKEN_KEY));
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const login = async (email: string, password: string) => {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch("/api/session/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        throw new Error("Invalid credentials");
      }

      const data = await res.json();
      localStorage.setItem(TOKEN_KEY, data.token);
      setIsLoggedIn(true);
      return true;
    } catch (err: any) {
      setError(err.message || "Login failed");
      setIsLoggedIn(false);
      return false;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem(TOKEN_KEY);
    setIsLoggedIn(false);
  };

  useEffect(() => {
    setIsLoggedIn(!!localStorage.getItem(TOKEN_KEY));
  }, []);

  return { isLoggedIn, login, logout, loading, error };
};