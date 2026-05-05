import styles from "./StateBlock.module.css";

function ErrorState({ message = "Something went wrong." }: { message?: string }) {
  return <div className={`${styles.block} ${styles.error}`}>{message}</div>;
}

export default ErrorState;

