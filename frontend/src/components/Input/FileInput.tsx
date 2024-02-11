import { ChangeEvent } from "react";
import styles from './FileInput.module.css';

interface FileInputProps {
  multiple?: boolean
  onChange: (value: any) => void
}

export const FileInput = (props: FileInputProps) => {
  const { multiple = false, onChange } = props

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    onChange(event.target.files)
  }

  return (
    <div className={styles["FileInputContainer"]}>
      <input className={styles["FileInput"]} type="file" multiple={multiple} onChange={handleChange} />
    </div>
    
  )
}
