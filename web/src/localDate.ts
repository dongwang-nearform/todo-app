export function localISODate(now = new Date()): string {
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

export function toHms(value: string): string {
  if (/^\d{2}:\d{2}$/.test(value)) return `${value}:00`
  return value
}
