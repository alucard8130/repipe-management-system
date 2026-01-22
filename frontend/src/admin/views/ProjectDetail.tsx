import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { fetchProject, generateClientLink } from "../../api/projects"

export default function ProjectDetail() {
  const { id } = useParams()
  const [project, setProject] = useState<any>(null)
  const [link, setLink] = useState<any>(null)

  useEffect(() => {
    if (id) {
      fetchProject(id).then(setProject)
    }
  }, [id])

  async function handleGenerateLink() {
    const data = await generateClientLink(Number(id))
    setLink(data)
  }

  if (!project) return <p>Loading...</p>

  return (
    <div className="space-y-8">
      {/* HEADER */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold">
            Project {project.project_number}
          </h1>
          <p className="text-sm text-gray-500">
            Status: <b>{project.status}</b>
          </p>
        </div>

        <button
          onClick={handleGenerateLink}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Generate Client Link
        </button>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <KPI title="Sale Price" value={`$${project.cost_summary.sale_price}`} />
        <KPI title="Cost" value={`$${project.cost_summary.total_cost}`} />
        <KPI title="Profit" value={`$${project.cost_summary.profit}`} />
        <KPI title="Margin" value={`${project.cost_summary.margin_percent}%`} />
      </div>

      {/* MILESTONES */}
      <Section title="Progress">
        <ul className="space-y-2">
          {project.milestones.map((m: any) => (
            <li
              key={m.id}
              className="flex justify-between bg-gray-50 p-3 rounded"
            >
              <span>{m.name}</span>
              <span className="font-semibold">{m.status}</span>
            </li>
          ))}
        </ul>
      </Section>

      {/* DOCUMENTS */}
      <Section title="Documents">
        <ul className="space-y-2">
          {project.documents.map((d: any) => (
            <li
              key={d.id}
              className="flex justify-between items-center border-b py-2"
            >
              <span>{d.file_name}</span>
              <span className="text-sm text-gray-500">
                {d.category}
              </span>
            </li>
          ))}
        </ul>
      </Section>

      {/* CLIENT ACCESS */}
      <Section title="Client Access">
        {link ? (
          <div className="bg-green-50 p-4 rounded">
            <p className="text-sm">Client Link:</p>
            <code className="text-xs break-all">{link.url}</code>
          </div>
        ) : (
          <p className="text-sm text-gray-500">
            No active client link
          </p>
        )}
      </Section>

      {/* BILLING */}
      <Section title="Billing">
        <ul className="space-y-2">
          {project.invoices.map((inv: any) => (
            <li key={inv.id} className="flex justify-between">
              <span>{inv.invoice_number}</span>
              <span>
                ${inv.balance} / ${inv.total}
              </span>
            </li>
          ))}
        </ul>
      </Section>
    </div>
  )
}

/* ===== Helpers ===== */

function KPI({ title, value }: { title: string; value: string }) {
  return (
    <div className="bg-white rounded shadow p-4">
      <p className="text-xs text-gray-500">{title}</p>
      <p className="text-xl font-bold">{value}</p>
    </div>
  )
}

function Section({
  title,
  children,
}: {
  title: string
  children: React.ReactNode
}) {
  return (
    <div className="bg-white rounded shadow p-4 space-y-4">
      <h2 className="font-bold">{title}</h2>
      {children}
    </div>
  )
}
