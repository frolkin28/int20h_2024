interface ButtonProps {
  text: string
  onClick: () => void
  disabled?: boolean;
}

export const Button = (props: ButtonProps) => {
  const { text, onClick, disabled } = props

  return (
    <button type="button" onClick={onClick} disabled={disabled}>
      {text}
    </button>
  )
}
