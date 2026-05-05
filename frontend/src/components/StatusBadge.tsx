import styles from "./StatusBadge.module.css";

interface StatusBadgeProps {
  label: string;
  variant: "success" | "danger" | "neutral" | "info";
}

function StatusBadge({ label, variant }: StatusBadgeProps) {
  return <span className={`${styles.badge} ${styles[variant]}`}>{label}</span>;
}

export default StatusBadge;

