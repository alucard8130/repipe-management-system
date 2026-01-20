import { useEffect, useState } from "react"
import api from "../api/client"

interface Material {
  id: number
  code: string
  name: string
  unit: string
  category: string
  stock: string
}

export default function Inventory() {
  const [materials, setMaterials] = useState<Material[]>([])
  const [loading, setLoading] = useState(true)
  const [quantity, setQuantity] = useState<Record<number, string>>({})

  useEffect(() => {
    api.get("/inventory/materials/")
      .then((res) => setMaterials(res.data.results))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  function consume(materialId: number) {
    const qty = quantity[materialId]
    if (!qty) return alert("Enter quantity")

    api.post("/inventory/consume/", {
      material_id: materialId,
      project_id: 1, // ⚠️ luego lo haces dinámico
      quantity: qty,
      reference_id: "UI-CONSUME",
    })
      .then(() => {
        alert("Material consumed")
        return api.get("/inventory/materials/")
      })
      .then((res) => setMaterials(res.data.results))
      .catch((err) => {
        alert(err.response?.data?.error || "Error")
      })
  }

  if (loading) return <p>Loading inventory...</p>

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Inventory</h1>

      <table className="w-full bg-white border">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-2 border">Code</th>
            <th className="p-2 border">Name</th>
            <th className="p-2 border">Category</th>
            <th className="p-2 border">Stock</th>
            <th className="p-2 border">Consume</th>
          </tr>
        </thead>
        <tbody>
          {materials.map((m) => (
            <tr key={m.id}>
              <td className="p-2 border">{m.code}</td>
              <td className="p-2 border">{m.name}</td>
              <td className="p-2 border">{m.category}</td>
              <td className="p-2 border font-bold">{m.stock}</td>
              <td className="p-2 border">
                <div className="flex gap-2">
                  <input
                    type="number"
                    className="border p-1 w-20"
                    placeholder="Qty"
                    value={quantity[m.id] || ""}
                    onChange={(e) =>
                      setQuantity({ ...quantity, [m.id]: e.target.value })
                    }
                  />
                  <button
                    onClick={() => consume(m.id)}
                    className="bg-blue-600 text-white px-2 rounded"
                  >
                    Use
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
