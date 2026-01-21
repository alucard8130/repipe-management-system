import { useParams } from "react-router-dom"
import { useEffect, useState } from "react"
import { fetchClientProject } from "../api/clientPortal"

export default function ClientProject() {
  const { token } = useParams()
  const [data, setData] = useState<any>(null)

  useEffect(() => {
    if (token) {
      fetchClientProject(token).then(setData)
    }
  }, [token])

  if (!data) return <p>Loading...</p>

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-bold">
        Project {data.project_number}
      </h1>

      <p>Status: <b>{data.status}</b></p>

      {/* Milestones */}
      <div>
        <h2 className="font-semibold">Progress</h2>
        <ul className="list-disc ml-5">
          {data.milestones.map((m: any) => (
            <li key={m.id}>
              {m.name} — {m.status}
            </li>
          ))}
        </ul>
      </div>

      {/* Documents */}
      <div>
        <h2 className="font-semibold">Documents</h2>
        <ul className="list-disc ml-5">
          {data.documents.map((d: any) => (
            <li key={d.id}>
              <a
                href={d.download_url}
                className="text-blue-600 underline"
              >
                {d.file_name}
              </a>
            </li>
          ))}
        </ul>
      </div>

      {/* Financials (if allowed) */}
      {data.financials && (
        <div>
          <h2 className="font-semibold">Financials</h2>
          <p>Total: ${data.financials.total}</p>
          <p>Balance: ${data.financials.balance}</p>
        </div>
      )}
    </div>
  )
}
