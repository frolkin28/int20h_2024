import { ChangeEvent } from "react";
import styles from './DateTimeInput.module.css'

interface DateTimeInputProps {
  id: string
  onChange: (value: string) => void
}

export const DateTimeInput = (props: DateTimeInputProps) => {
  const {id, onChange} = props

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    onChange(new Date(event.target.value).toISOString())
  }

  return (
    <input className={styles["DateTimeInput"]} type="datetime-local" id={id} onChange={handleChange} />
  )
}
