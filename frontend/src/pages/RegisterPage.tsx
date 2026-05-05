import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { UserRole } from "../types";
import styles from "./Auth.module.css";

function RegisterPage() {
  const navigate = useNavigate();
  const { registerUser } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<UserRole>("TRAINEE");
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
      await registerUser({ email, password, role });
      navigate("/dashboard", { replace: true });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Register failed");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className={styles.wrapper}>
      <div className={styles.card}>
        <h1 className={styles.title}>Register</h1>
        <p className={styles.subtitle}>Create your account and start tracking.</p>
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

          <label className={styles.label}>
            Role
            <select className={styles.select} value={role} onChange={(event) => setRole(event.target.value as UserRole)}>
              <option value="TRAINEE">TRAINEE</option>
              <option value="TRAINER">TRAINER</option>
            </select>
          </label>

          {error ? <p className={styles.error}>{error}</p> : null}
          <button className={styles.button} type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Creating..." : "Register"}
          </button>
        </form>
        <p className={styles.linkLine}>
          Already registered?{" "}
          <Link className={styles.link} to="/login">
            Go to login
          </Link>
        </p>
      </div>
    </div>
  );
}

export default RegisterPage;

