import styles from "./StateBlock.module.css";

function EmptyState({ message = "No data available." }: { message?: string }) {
  return <div className={styles.block}>{message}</div>;
}

export default EmptyState;

