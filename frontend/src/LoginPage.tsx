import { useEffect, useState } from "react";
import type { SyntheticEvent } from "react";
import { api, type LoginResponse, type UserOut } from "./api";

export function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [user, setUser] = useState<UserOut | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api<UserOut>("/auth/me")
      .then((me) => setUser(me))
      .catch(() => setUser(null));
  }, []);

  async function handleLogin(e: SyntheticEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const res = await api<LoginResponse>("/auth/login", {
        method: "POST",
        body: JSON.stringify({
          username,
          password,
        }),
      });

      setUser(res.user);
      setPassword("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Не удалось войти");
    } finally {
      setLoading(false);
    }
  }

  async function handleLogout() {
    try {
      await api("/auth/logout", {
        method: "POST",
      });
    } finally {
      setUser(null);
    }
  }

  if (user) {
    return (
      <div className="page">
        <div className="box">
          <h2>Вход выполнен</h2>

          <p>
            Пользователь: <b>{user.username}</b>
          </p>

          <p>
            Роляша: <b>{user.role}</b>
          </p>

          <button onClick={handleLogout}>Выйти</button>
        </div>
      </div>
    );
  }

  return (
    <div className="page">
      <form className="box" onSubmit={handleLogin}>
        <h2>Вход</h2>

        <label>
          Логин
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
            required
          />
        </label>

        <label>
          Пароль
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
            required
          />
        </label>

        {error && <div className="error">{error}</div>}

        <button type="submit" disabled={loading}>
          {loading ? "Входим..." : "Войти"}
        </button>
      </form>
    </div>
  );
}
