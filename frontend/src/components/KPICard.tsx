type Props = {
  title: string
  value: string | number
  subtitle?: string
}

export default function KPICard({ title, value, subtitle }: Props) {
  return (
    <div className="bg-white rounded shadow p-4">
      <p className="text-sm text-gray-500">{title}</p>
      <p className="text-2xl font-bold">{value}</p>
      {subtitle && <p className="text-xs text-gray-400">{subtitle}</p>}
    </div>
  )
}
