import { useEffect, useState } from "react"
import { fetchMaterials, consumeMaterial } from "../api/inventory"
import api from "../api/client"

type Material = {
  id: number
  code: string
  name: string
  unit: string
  stock: string
}

type Project = {
  id: number
  project_number: string
}

export default function Inventory() {
  const [materials, setMaterials] = useState<Material[]>([])
  const [projects, setProjects] = useState<Project[]>([])
  const [selectedMaterial, setSelectedMaterial] = useState<Material | null>(null)
  const [quantity, setQuantity] = useState("")
  const [projectId, setProjectId] = useState("")
  const [message, setMessage] = useState("")

  useEffect(() => {
    fetchMaterials().then(setMaterials)
    api.get("/projects/").then((res) => setProjects(res.data.results))
  }, [])

  async function handleConsume() {
    if (!selectedMaterial || !projectId || !quantity) return

    try {
      await consumeMaterial({
        material_id: selectedMaterial.id,
        project_id: Number(projectId),
        quantity,
        reference_id: "UI",
        notes: "Consumed from Inventory UI",
      })

      setMessage("Material consumed successfully")
      setQuantity("")
      setSelectedMaterial(null)
      fetchMaterials().then(setMaterials)
    } catch (err: any) {
      setMessage(err.response?.data?.error || "Error consuming material")
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Inventory</h1>

      {message && <p className="text-sm text-blue-600">{message}</p>}

      {/* Materials table */}
      <div className="bg-white rounded shadow p-4">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b text-left">
              <th>Code</th>
              <th>Name</th>
              <th>Stock</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {materials.map((m) => (
              <tr key={m.id} className="border-b">
                <td className="py-2">{m.code}</td>
                <td>{m.name}</td>
                <td>{m.stock}</td>
                <td>
                  <button
                    className="text-blue-600 hover:underline"
                    onClick={() => setSelectedMaterial(m)}
                  >
                    Consume
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Consume modal */}
      {selectedMaterial && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
          <div className="bg-white p-6 rounded w-96 space-y-4">
            <h2 className="font-bold">
              Consume {selectedMaterial.name}
            </h2>

            <input
              type="number"
              placeholder="Quantity"
              className="w-full border p-2 rounded"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
            />

            <select
              className="w-full border p-2 rounded"
              value={projectId}
              onChange={(e) => setProjectId(e.target.value)}
            >
              <option value="">Select Project</option>
              {projects.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.project_number}
                </option>
              ))}
            </select>

            <div className="flex justify-end gap-2">
              <button
                onClick={() => setSelectedMaterial(null)}
                className="px-3 py-1 border rounded"
              >
                Cancel
              </button>
              <button
                onClick={handleConsume}
                className="px-3 py-1 bg-blue-600 text-white rounded"
              >
                Consume
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
