import { ChangeEvent } from "react";

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
    <input type="file" multiple={multiple} onChange={handleChange} />
  )
}
