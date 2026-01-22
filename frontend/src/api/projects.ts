import api from "./client"

export async function fetchProject(id: string) {
  const res = await api.get(`/projects/${id}/`)
  return res.data
}

export async function generateClientLink(projectId: number) {
  const res = await api.post(`/projects/${projectId}/client-link/`)
  return res.data
}
