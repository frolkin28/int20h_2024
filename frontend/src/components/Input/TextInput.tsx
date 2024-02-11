import React, { useState, ChangeEvent } from "react";
import styles from "./TextInput.module.css";

interface TextInputProps {
  id: string
  value: string
  onChange: (value: string) => void
  placeholder?: string
  type?: "text" | "password"
  className?: string;
}

export const TextInput = (props: TextInputProps) => {
  const { id, value, onChange, placeholder, type = "text" } = props

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    onChange(event.target.value)
  }

  return (
    <input
      id={id}
      type={type}
      value={value}
      onChange={handleChange}
      placeholder={placeholder}
      className={styles["form-input"]}
    />
  )
}