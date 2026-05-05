import { FormEvent, useEffect, useMemo, useState } from "react";
import EmptyState from "../components/EmptyState";
import ErrorState from "../components/ErrorState";
import LoadingState from "../components/LoadingState";
import { useAuth } from "../hooks/useAuth";
import { createActivity, getActivities } from "../services/activities";
import { Activity } from "../types";
import styles from "./PageShared.module.css";

function ActivitiesPage() {
  const { user } = useAuth();
  const [activities, setActivities] = useState<Activity[]>([]);
  const [durationMinutes, setDurationMinutes] = useState<number>(30);
  const [activityType, setActivityType] = useState("cardio");
  const [date, setDate] = useState<string>(new Date().toISOString().split("T")[0]);
  const [typeFilter, setTypeFilter] = useState("");
  const [dateFilter, setDateFilter] = useState("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formError, setFormError] = useState<string | null>(null);

  const fetchActivities = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await getActivities();
      setActivities(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load activities");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void fetchActivities();
  }, []);

  const filteredActivities = useMemo(() => {
    return activities.filter((activity) => {
      const matchesType = typeFilter
        ? activity.activity_type.toLowerCase().includes(typeFilter.toLowerCase())
        : true;
      const matchesDate = dateFilter ? activity.date === dateFilter : true;
      return matchesType && matchesDate;
    });
  }, [activities, dateFilter, typeFilter]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setFormError(null);

    if (!user) {
      setFormError("Current user not found.");
      return;
    }
    if (!activityType.trim()) {
      setFormError("Activity type is required.");
      return;
    }
    if (durationMinutes <= 0) {
      setFormError("Duration must be greater than 0.");
      return;
    }
    if (date > new Date().toISOString().split("T")[0]) {
      setFormError("Date cannot be in the future.");
      return;
    }

    try {
      setSubmitting(true);
      await createActivity({
        user_id: user.id,
        duration_minutes: durationMinutes,
        activity_type: activityType,
        date
      });
      await fetchActivities();
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Could not create activity");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className={styles.page}>
      <div>
        <h1 className={styles.title}>Activities</h1>
        <p className={styles.subtitle}>Create activity logs and review history with filters.</p>
      </div>

      <section className={styles.panel}>
        <form className={styles.formGrid} onSubmit={handleSubmit}>
          <label className={styles.label}>
            User ID
            <input className={styles.input} value={user?.id ?? ""} readOnly />
          </label>

          <label className={styles.label}>
            Duration (minutes)
            <input
              className={styles.input}
              type="number"
              min={1}
              value={durationMinutes}
              onChange={(event) => setDurationMinutes(Number(event.target.value))}
              required
            />
          </label>

          <label className={styles.label}>
            Activity Type
            <input
              className={styles.input}
              value={activityType}
              onChange={(event) => setActivityType(event.target.value)}
              required
            />
          </label>

          <label className={styles.label}>
            Date
            <input className={styles.input} type="date" value={date} onChange={(event) => setDate(event.target.value)} required />
          </label>

          <button className={styles.button} type="submit" disabled={submitting}>
            {submitting ? "Saving..." : "Create Activity"}
          </button>
        </form>
        {formError ? <p className={styles.error}>{formError}</p> : null}
      </section>

      <section className={styles.panel}>
        <div className={styles.formGrid}>
          <label className={styles.label}>
            Filter by Type
            <input
              className={styles.input}
              placeholder="cardio"
              value={typeFilter}
              onChange={(event) => setTypeFilter(event.target.value)}
            />
          </label>

          <label className={styles.label}>
            Filter by Date
            <input
              className={styles.input}
              type="date"
              value={dateFilter}
              onChange={(event) => setDateFilter(event.target.value)}
            />
          </label>
        </div>
      </section>

      {loading ? <LoadingState message="Loading activities..." /> : null}
      {error ? <ErrorState message={error} /> : null}

      {!loading && !error ? (
        <section className={styles.panel}>
          {filteredActivities.length ? (
            <div className={styles.tableWrap}>
              <table className={styles.table}>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>User ID</th>
                    <th>Type</th>
                    <th>Duration</th>
                    <th>Date</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredActivities.map((activity) => (
                    <tr key={activity.id}>
                      <td>{activity.id}</td>
                      <td>{activity.user_id}</td>
                      <td>{activity.activity_type}</td>
                      <td>{activity.duration_minutes} min</td>
                      <td>{activity.date}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <EmptyState message="No activities found for the current filters." />
          )}
        </section>
      ) : null}
    </div>
  );
}

export default ActivitiesPage;

