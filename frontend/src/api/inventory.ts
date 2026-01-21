import api from "./client"

export async function fetchMaterials() {
  const res = await api.get("/inventory/materials/")
  return res.data.results
}

export async function fetchMovements() {
  const res = await api.get("/inventory/movements/")
  return res.data.results
}

export async function consumeMaterial(payload: {
  material_id: number
  project_id: number
  quantity: string
  reference_id?: string
  notes?: string
}) {
  const res = await api.post("/inventory/consume/", payload)
  return res.data
}
