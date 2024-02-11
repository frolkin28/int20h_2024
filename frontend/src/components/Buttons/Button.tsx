import styles from './Button.module.css';

interface ButtonProps {
  text: string
  onClick: () => void
  disabled?: boolean;
}

export const Button = (props: ButtonProps) => {
  const { text, onClick, disabled } = props

  return (
    <button className={styles["my-button"]} type="button" onClick={onClick} disabled={disabled}>
      {text}
    </button>
  )
}
