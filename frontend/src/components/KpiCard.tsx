import styles from "./KpiCard.module.css";

interface KpiCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
}

function KpiCard({ title, value, subtitle }: KpiCardProps) {
  return (
    <div className={styles.card}>
      <p className={styles.title}>{title}</p>
      <p className={styles.value}>{value}</p>
      {subtitle ? <p className={styles.subtitle}>{subtitle}</p> : null}
    </div>
  );
}

export default KpiCard;

