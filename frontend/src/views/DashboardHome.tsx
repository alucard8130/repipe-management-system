import { useEffect, useState } from "react"
import KPICard from "../components/KPICard"
import { fetchProjects } from "../api/dashboard"

type Project = {
  id: number
  project_number: string
  status: string
  cost_summary: {
    sale_price: string
    total_cost: string
    profit: string
    margin_percent: string
  }
}

export default function DashboardHome() {
  const [projects, setProjects] = useState<Project[]>([])

  useEffect(() => {
    fetchProjects().then(setProjects).catch(console.error)
  }, [])

  const totalRevenue = projects.reduce(
    (acc, p) => acc + Number(p.cost_summary.sale_price),
    0
  )

  const totalProfit = projects.reduce(
    (acc, p) => acc + Number(p.cost_summary.profit),
    0
  )

  const avgMargin =
    projects.length > 0
      ? (
          projects.reduce(
            (acc, p) => acc + Number(p.cost_summary.margin_percent),
            0
          ) / projects.length
        ).toFixed(2)
      : "0.00"

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>

      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <KPICard title="Revenue" value={`$${totalRevenue.toFixed(2)}`} />
        <KPICard title="Profit" value={`$${totalProfit.toFixed(2)}`} />
        <KPICard title="Avg Margin" value={`${avgMargin}%`} />
      </div>

      {/* Projects table */}
      <div className="bg-white rounded shadow p-4">
        <h2 className="font-bold mb-3">Projects</h2>

        <table className="w-full text-sm">
          <thead>
            <tr className="text-left border-b">
              <th>Project</th>
              <th>Status</th>
              <th>Margin</th>
              <th>Profit</th>
            </tr>
          </thead>
          <tbody>
            {projects.map((p) => (
              <tr key={p.id} className="border-b">
                <td className="py-2">{p.project_number}</td>
                <td>{p.status}</td>
                <td
                  className={
                    Number(p.cost_summary.margin_percent) < 20
                      ? "text-red-600 font-semibold"
                      : ""
                  }
                >
                  {p.cost_summary.margin_percent}%
                </td>
                <td>${p.cost_summary.profit}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
