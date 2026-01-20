import { useEffect, useState } from "react"
import api from "../api/client"

interface Project {
  id: number
  project_number: string
  title: string
  status: string
  cost_summary: {
    sale_price: string
    total_cost: string
    profit: string
    margin_percent: string
  }
}

export default function Projects() {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get("/projects/")
      .then((res) => setProjects(res.data.results))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <p>Loading projects...</p>

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Projects</h1>

      <div className="grid gap-4">
        {projects.map((p) => (
          <div
            key={p.id}
            className="bg-white p-4 rounded shadow border"
          >
            <div className="flex justify-between">
              <div>
                <h2 className="font-semibold">
                  {p.project_number} — {p.title}
                </h2>
                <p className="text-sm text-gray-600">
                  Status: {p.status}
                </p>
              </div>

              <div className="text-right">
                <p className="text-sm">
                  Margin
                </p>
                <p
                  className={`font-bold ${
                    Number(p.cost_summary.margin_percent) < 20
                      ? "text-red-600"
                      : "text-green-600"
                  }`}
                >
                  {p.cost_summary.margin_percent} %
                </p>
              </div>
            </div>

            <div className="mt-2 text-sm text-gray-700">
              <p>Sale: ${p.cost_summary.sale_price}</p>
              <p>Cost: ${p.cost_summary.total_cost}</p>
              <p>Profit: ${p.cost_summary.profit}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
