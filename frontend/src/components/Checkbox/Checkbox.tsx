import { ChangeEvent } from "react"

interface CheckboxProps {
  id: string
  checked: boolean
  onChange: () => void
}

export const Checkbox = (props: CheckboxProps) => {
  const { id, checked, onChange } = props

  return (
    <input
      type="checkbox"
      id={id}
      checked={checked}
      onChange={onChange}
    />
  )
}
