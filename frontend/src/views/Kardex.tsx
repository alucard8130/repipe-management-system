import { useEffect, useState } from "react"
import { fetchMovements } from "../api/inventory"

type Movement = {
  id: number
  movement_type: "IN" | "OUT" | "ADJUST"
  material_code: string
  quantity: string
  unit_cost: string
  total_cost: string
  reference_type: string
  reference_id: string
  created_at: string
}

export default function Kardex() {
  const [movements, setMovements] = useState<Movement[]>([])

  useEffect(() => {
    fetchMovements().then(setMovements).catch(console.error)
  }, [])

  function badge(type: string) {
    if (type === "IN") return "bg-green-100 text-green-800"
    if (type === "OUT") return "bg-red-100 text-red-800"
    return "bg-yellow-100 text-yellow-800"
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Kardex</h1>

      <div className="bg-white rounded shadow p-4 overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b text-left">
              <th>Date</th>
              <th>Material</th>
              <th>Type</th>
              <th>Qty</th>
              <th>Unit Cost</th>
              <th>Total Cost</th>
              <th>Reference</th>
            </tr>
          </thead>
          <tbody>
            {movements.map((m) => (
              <tr key={m.id} className="border-b">
                <td className="py-2">
                  {new Date(m.created_at).toLocaleDateString()}
                </td>
                <td>{m.material_code}</td>
                <td>
                  <span
                    className={`px-2 py-1 rounded text-xs font-semibold ${badge(
                      m.movement_type
                    )}`}
                  >
                    {m.movement_type}
                  </span>
                </td>
                <td>{m.quantity}</td>
                <td>${m.unit_cost}</td>
                <td className="font-semibold">${m.total_cost}</td>
                <td>
                  {m.reference_type} {m.reference_id}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
