import { ChangeEvent } from "react";

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
    <textarea id={id} value={value} onChange={handleChange} />
  )
}
