import styles from "./StateBlock.module.css";

function LoadingState({ message = "Loading..." }: { message?: string }) {
  return <div className={styles.block}>{message}</div>;
}

export default LoadingState;

