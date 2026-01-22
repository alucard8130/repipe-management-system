import { useEffect, useState } from "react"
import api from "../../api/client"
import { Link } from "react-router-dom"

export default function ProjectsAdmin() {
  const [projects, setProjects] = useState<any[]>([])

  useEffect(() => {
    api.get("/projects/").then((res) => setProjects(res.data.results))
  }, [])

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-bold">Projects</h1>

      <div className="bg-white rounded shadow">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b text-left">
              <th className="p-3">Project</th>
              <th>Status</th>
              <th>Company</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {projects.map((p) => (
              <tr key={p.id} className="border-b">
                <td className="p-3">{p.project_number}</td>
                <td>{p.status}</td>
                <td>{p.company_name}</td>
                <td>
                  <Link
                    to={`/admin/projects/${p.id}`}
                    className="text-blue-600 hover:underline"
                  >
                    Open
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
