import { useEffect, useMemo, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import EmptyState from "../components/EmptyState";
import ErrorState from "../components/ErrorState";
import KpiCard from "../components/KpiCard";
import LoadingState from "../components/LoadingState";
import { getActivities } from "../services/activities";
import { getTrainerLoad, getTrainerRanking, getUserSummary } from "../services/analytics";
import { getUsers } from "../services/users";
import { Activity, RankingItem, TrainerLoad, UserSummary } from "../types";
import styles from "./PageShared.module.css";

const PIE_COLORS = ["#2563eb", "#60a5fa", "#22c55e", "#f59e0b", "#f97316", "#8b5cf6", "#06b6d4", "#ef4444"];

function DashboardPage() {
  const [usersCount, setUsersCount] = useState(0);
  const [activities, setActivities] = useState<Activity[]>([]);
  const [ranking, setRanking] = useState<RankingItem[]>([]);
  const [trainerLoad, setTrainerLoad] = useState<TrainerLoad[]>([]);
  const [userSummary, setUserSummary] = useState<UserSummary[]>([]);
  const [activeTrainers, setActiveTrainers] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      setLoading(true);
      setError(null);
      try {
        const [users, activitiesData, rankingData, loadData, summaryData] = await Promise.all([
          getUsers(),
          getActivities(),
          getTrainerRanking(),
          getTrainerLoad(),
          getUserSummary()
        ]);

        setUsersCount(users.length);
        setActivities(activitiesData);
        setRanking(rankingData);
        setTrainerLoad(loadData);
        setUserSummary(summaryData);
        setActiveTrainers(users.filter((user) => user.role === "TRAINER" && user.is_active).length);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load dashboard data");
      } finally {
        setLoading(false);
      }
    };

    void fetchDashboard();
  }, []);

  const avgDuration = useMemo(() => {
    const totalActivities = userSummary.reduce((acc, item) => acc + item.total_activities, 0);
    if (!totalActivities) {
      return 0;
    }
    const weightedTotal = userSummary.reduce(
      (acc, item) => acc + item.total_activities * item.average_duration_minutes,
      0
    );
    return weightedTotal / totalActivities;
  }, [userSummary]);

  return (
    <div className={styles.page}>
      <div>
        <h1 className={styles.title}>Analytics Dashboard</h1>
        <p className={styles.subtitle}>Business and performance overview from live API data.</p>
      </div>

      {loading ? <LoadingState message="Loading dashboard..." /> : null}
      {error ? <ErrorState message={error} /> : null}

      {!loading && !error ? (
        <>
          <section className={styles.grid4}>
            <KpiCard title="Total Users" value={usersCount} />
            <KpiCard title="Total Activities" value={activities.length} />
            <KpiCard title="Average Duration" value={`${avgDuration.toFixed(1)} min`} />
            <KpiCard title="Active Trainers" value={activeTrainers} />
          </section>

          <section className={styles.grid2}>
            <div className={styles.panel}>
              <h3>Trainer Ranking</h3>
              {ranking.length ? (
                <ResponsiveContainer width="100%" height={280}>
                  <BarChart data={ranking}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="trainer_email" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="total_duration_minutes" fill="#2563eb" name="Total Minutes" />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <EmptyState message="No ranking data available." />
              )}
            </div>

            <div className={styles.panel}>
              <h3>Weekly Trainer Load</h3>
              {trainerLoad.length ? (
                <ResponsiveContainer width="100%" height={280}>
                  <LineChart
                    data={trainerLoad.map((item) => ({
                      ...item,
                      week: `${item.week_start} - ${item.week_end}`
                    }))}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="week" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line
                      dataKey="total_duration_minutes"
                      name="Duration (min)"
                      stroke="#0ea5e9"
                      strokeWidth={2}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <EmptyState message="No weekly load data available." />
              )}
            </div>
          </section>

          <section className={styles.panel}>
            <h3>User Activity Summary</h3>
            {userSummary.length ? (
              <ResponsiveContainer width="100%" height={320}>
                <PieChart>
                  <Pie
                    data={userSummary}
                    dataKey="total_activities"
                    nameKey="user_email"
                    outerRadius={115}
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  >
                    {userSummary.map((item, index) => (
                      <Cell key={item.user_id} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <EmptyState message="No user summary data available." />
            )}
          </section>
        </>
      ) : null}
    </div>
  );
}

export default DashboardPage;

