type Props = {
  label: string
  value?: number
}

export default function StatisticItem({ label, value = 0 }: Props) {
  return (
    <div className="grid grid-cols-2 gap-2">
      <p>{label}</p>
      <p className="text-xl font-medium">{value} 📰</p>
    </div>
  )
}
