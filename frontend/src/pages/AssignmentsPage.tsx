import { FormEvent, useEffect, useMemo, useState } from "react";
import EmptyState from "../components/EmptyState";
import ErrorState from "../components/ErrorState";
import LoadingState from "../components/LoadingState";
import { createAssignment, getAssignments } from "../services/assignments";
import { getUsers } from "../services/users";
import { Assignment, User } from "../types";
import styles from "./PageShared.module.css";

function AssignmentsPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [assignments, setAssignments] = useState<Assignment[]>([]);
  const [traineeId, setTraineeId] = useState<number | "">("");
  const [trainerId, setTrainerId] = useState<number | "">("");
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formError, setFormError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [usersData, assignmentsData] = await Promise.all([getUsers(), getAssignments()]);
      setUsers(usersData);
      setAssignments(assignmentsData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load assignments data");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void fetchData();
  }, []);

  const trainees = useMemo(() => users.filter((user) => user.role === "TRAINEE"), [users]);
  const trainers = useMemo(() => users.filter((user) => user.role === "TRAINER"), [users]);

  const usersById = useMemo(() => {
    return users.reduce<Record<number, User>>((acc, user) => {
      acc[user.id] = user;
      return acc;
    }, {});
  }, [users]);

  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setFormError(null);
    if (!traineeId || !trainerId) {
      setFormError("Please select both trainee and trainer.");
      return;
    }
    if (traineeId === trainerId) {
      setFormError("Trainee and trainer must be different users.");
      return;
    }

    try {
      setSubmitting(true);
      await createAssignment({ trainee_id: traineeId, trainer_id: trainerId });
      setTraineeId("");
      setTrainerId("");
      await fetchData();
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Could not create assignment");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className={styles.page}>
      <div>
        <h1 className={styles.title}>Assignments</h1>
        <p className={styles.subtitle}>Link trainees to trainers and track relationships.</p>
      </div>

      <section className={styles.panel}>
        <form className={styles.formGrid} onSubmit={onSubmit}>
          <label className={styles.label}>
            Trainee
            <select
              className={styles.select}
              value={traineeId}
              onChange={(event) => setTraineeId(event.target.value ? Number(event.target.value) : "")}
            >
              <option value="">Select trainee</option>
              {trainees.map((trainee) => (
                <option key={trainee.id} value={trainee.id}>
                  {trainee.email}
                </option>
              ))}
            </select>
          </label>

          <label className={styles.label}>
            Trainer
            <select
              className={styles.select}
              value={trainerId}
              onChange={(event) => setTrainerId(event.target.value ? Number(event.target.value) : "")}
            >
              <option value="">Select trainer</option>
              {trainers.map((trainer) => (
                <option key={trainer.id} value={trainer.id}>
                  {trainer.email}
                </option>
              ))}
            </select>
          </label>

          <button className={styles.button} type="submit" disabled={submitting}>
            {submitting ? "Assigning..." : "Create Assignment"}
          </button>
        </form>
        {formError ? <p className={styles.error}>{formError}</p> : null}
      </section>

      {loading ? <LoadingState message="Loading assignments..." /> : null}
      {error ? <ErrorState message={error} /> : null}

      {!loading && !error ? (
        <section className={styles.panel}>
          {assignments.length ? (
            <div className={styles.tableWrap}>
              <table className={styles.table}>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Trainee</th>
                    <th>Trainer</th>
                  </tr>
                </thead>
                <tbody>
                  {assignments.map((assignment) => (
                    <tr key={assignment.id}>
                      <td>{assignment.id}</td>
                      <td>{usersById[assignment.trainee_id]?.email ?? assignment.trainee_id}</td>
                      <td>{usersById[assignment.trainer_id]?.email ?? assignment.trainer_id}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <EmptyState message="No assignments yet." />
          )}
        </section>
      ) : null}
    </div>
  );
}

export default AssignmentsPage;

