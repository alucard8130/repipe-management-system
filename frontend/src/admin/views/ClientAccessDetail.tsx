import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import {
  fetchClientLinks,
  generateClientLink,
  revokeClientLink,
} from "../../api/clients"

export default function ClientAccessDetail() {
  const { id } = useParams()
  const [links, setLinks] = useState<any[]>([])
  const [days, setDays] = useState(7)
  const [financials, setFinancials] = useState(false)

  useEffect(() => {
    if (id) {
      fetchClientLinks(Number(id)).then(setLinks)
    }
  }, [id])

  async function handleGenerate(projectId: number) {
    await generateClientLink(projectId, {
      expires_days: days,
      can_view_financials: financials,
    })
    fetchClientLinks(projectId).then(setLinks)
  }

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-bold">Client Access</h1>

      <div className="bg-white p-4 rounded shadow space-y-3">
        <h2 className="font-semibold">Generate Link</h2>

        <input
          type="number"
          className="border p-2 rounded"
          value={days}
          onChange={(e) => setDays(Number(e.target.value))}
        />

        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={financials}
            onChange={(e) => setFinancials(e.target.checked)}
          />
          Allow financials
        </label>

        <button
          onClick={() => handleGenerate(Number(id))}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Generate Link
        </button>
      </div>

      <div className="bg-white rounded shadow">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b">
              <th className="p-3">Token</th>
              <th>Expires</th>
              <th>Financials</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {links.map((l) => (
              <tr key={l.id} className="border-b">
                <td className="p-3 text-xs break-all">{l.token_hash}</td>
                <td>{l.expires_at}</td>
                <td>{l.can_view_financials ? "Yes" : "No"}</td>
                <td className="text-right">
                  <button
                    onClick={() =>
                      revokeClientLink(l.id).then(() =>
                        fetchClientLinks(Number(id)).then(setLinks)
                      )
                    }
                    className="text-red-600 hover:underline"
                  >
                    Revoke
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
