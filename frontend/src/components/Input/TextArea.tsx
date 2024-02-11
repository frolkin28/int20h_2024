import { ChangeEvent } from "react";
import styles from './TextArea.module.css';

interface TextAreaProps {
  id: string
  value: string
  onChange: (value: string) => void
}

export const TextArea = (props: TextAreaProps) => {
  const { id, value, onChange } = props

  const handleChange = (event: ChangeEvent<HTMLTextAreaElement>) => {
    onChange(event.target.value)
  }

  return (
    <textarea className={styles["TextArea"]} id={id} value={value} onChange={handleChange} />
  )
}
