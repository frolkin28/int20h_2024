export const transformDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleString('uk-UA', {
    timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}
