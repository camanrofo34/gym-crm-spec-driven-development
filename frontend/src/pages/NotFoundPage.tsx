import { Link } from "react-router-dom";

function NotFoundPage() {
  return (
    <main
      style={{
        minHeight: "100vh",
        display: "grid",
        placeItems: "center",
        background: "#f8fafc",
        fontFamily: "Inter, system-ui, sans-serif"
      }}
    >
      <div style={{ textAlign: "center" }}>
        <h1 style={{ margin: "0 0 .5rem" }}>404</h1>
        <p style={{ margin: "0 0 1rem", color: "#64748b" }}>Page not found.</p>
        <Link to="/dashboard">Go to dashboard</Link>
      </div>
    </main>
  );
}

export default NotFoundPage;

