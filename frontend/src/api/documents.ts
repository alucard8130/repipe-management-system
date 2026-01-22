import api from "./client"

export async function fetchDocuments(projectId?: number) {
  const url = projectId
    ? `/documents/?project=${projectId}`
    : "/documents/"
  const res = await api.get(url)
  return res.data.results
}

export async function uploadDocument(payload: FormData) {
  const res = await api.post("/documents/", payload, {
    headers: { "Content-Type": "multipart/form-data" },
  })
  return res.data
}

export async function toggleVisibility(id: number, visible: boolean) {
  const res = await api.patch(`/documents/${id}/`, {
    visible_to_client: visible,
  })
  return res.data
}
