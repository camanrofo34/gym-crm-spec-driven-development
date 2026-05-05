import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import styles from "./AppLayout.module.css";

function AppLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <div className={styles.container}>
      <aside className={styles.sidebar}>
        <h1 className={styles.brand}>Gym CRM</h1>
        <nav className={styles.nav}>
          <NavLink className={({ isActive }) => (isActive ? styles.active : styles.link)} to="/dashboard">
            Dashboard
          </NavLink>
          <NavLink className={({ isActive }) => (isActive ? styles.active : styles.link)} to="/users">
            Users
          </NavLink>
          <NavLink className={({ isActive }) => (isActive ? styles.active : styles.link)} to="/activities">
            Activities
          </NavLink>
          <NavLink className={({ isActive }) => (isActive ? styles.active : styles.link)} to="/assignments">
            Assignments
          </NavLink>
        </nav>
        <button className={styles.logout} onClick={handleLogout}>
          Logout
        </button>
      </aside>

      <main className={styles.main}>
        <header className={styles.header}>
          <div>
            <p className={styles.caption}>Welcome back</p>
            <h2 className={styles.title}>{user?.email ?? "User"}</h2>
          </div>
          <span className={styles.role}>{user?.role ?? "-"}</span>
        </header>
        <section className={styles.content}>
          <Outlet />
        </section>
      </main>
    </div>
  );
}

export default AppLayout;

