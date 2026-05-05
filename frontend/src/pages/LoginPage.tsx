import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import styles from "./Auth.module.css";

function LoginPage() {
  const navigate = useNavigate();
  const { loginWithCredentials } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    if (!email.trim() || password.length < 6) {
      setError("Please enter a valid email and password (min 6 characters).");
      return;
    }

    try {
      setIsSubmitting(true);
      await loginWithCredentials({ email, password });
      navigate("/dashboard", { replace: true });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.card}>
        <h1 className={styles.title}>Login</h1>
        <p className={styles.subtitle}>Access your gym analytics dashboard.</p>
        <form className={styles.form} onSubmit={onSubmit}>
          <label className={styles.label}>
            Email
            <input
              className={styles.input}
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
            />
          </label>

          <label className={styles.label}>
            Password
            <input
              className={styles.input}
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              minLength={6}
              required
            />
          </label>

          {error ? <p className={styles.error}>{error}</p> : null}
          <button className={styles.button} type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Signing in..." : "Login"}
          </button>
        </form>
        <p className={styles.linkLine}>
          New user?{" "}
          <Link className={styles.link} to="/register">
            Register here
          </Link>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;

