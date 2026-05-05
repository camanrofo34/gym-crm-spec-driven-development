import { useEffect, useMemo, useState } from "react";
import EmptyState from "../components/EmptyState";
import ErrorState from "../components/ErrorState";
import LoadingState from "../components/LoadingState";
import StatusBadge from "../components/StatusBadge";
import { getUsers } from "../services/users";
import { User } from "../types";
import styles from "./PageShared.module.css";

function UsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await getUsers();
        setUsers(response);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load users");
      } finally {
        setLoading(false);
      }
    };

    void fetchUsers();
  }, []);

  const filteredUsers = useMemo(() => {
    if (!query.trim()) {
      return users;
    }
    return users.filter((user) => user.email.toLowerCase().includes(query.toLowerCase()));
  }, [query, users]);

  return (
    <div className={styles.page}>
      <div>
        <h1 className={styles.title}>Users</h1>
        <p className={styles.subtitle}>User directory with active status and role visibility.</p>
      </div>

      <section className={styles.panel}>
        <label className={styles.label}>
          Search by email
          <input
            className={styles.input}
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="trainer@example.com"
          />
        </label>
      </section>

      {loading ? <LoadingState message="Loading users..." /> : null}
      {error ? <ErrorState message={error} /> : null}

      {!loading && !error ? (
        <section className={styles.panel}>
          {filteredUsers.length ? (
            <div className={styles.tableWrap}>
              <table className={styles.table}>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Status</th>
                    <th>Created</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredUsers.map((user) => (
                    <tr key={user.id}>
                      <td>{user.id}</td>
                      <td>{user.email}</td>
                      <td>
                        <StatusBadge label={user.role} variant={user.role === "TRAINER" ? "info" : "neutral"} />
                      </td>
                      <td>
                        <StatusBadge label={user.is_active ? "Active" : "Inactive"} variant={user.is_active ? "success" : "danger"} />
                      </td>
                      <td>{new Date(user.created_at).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <EmptyState message="No users match your search." />
          )}
        </section>
      ) : null}
    </div>
  );
}

export default UsersPage;

