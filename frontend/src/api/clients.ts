import api from "./client"

export async function fetchClients() {
  const res = await api.get("/clients/")
  return res.data.results
}

export async function createClient(payload: {
  email: string
  name: string
}) {
  const res = await api.post("/clients/", payload)
  return res.data
}

export async function toggleClient(id: number, active: boolean) {
  const res = await api.patch(`/clients/${id}/`, {
    is_active: active,
  })
  return res.data
}

export async function fetchClientLinks(projectId: number) {
  const res = await api.get(`/projects/${projectId}/client-links/`)
  return res.data
}

export async function generateClientLink(
  projectId: number,
  payload: {
    expires_days: number
    can_view_financials: boolean
  }
) {
  const res = await api.post(
    `/projects/${projectId}/client-links/`,
    payload
  )
  return res.data
}

export async function revokeClientLink(linkId: number) {
  const res = await api.patch(`/client-links/${linkId}/revoke/`)
  return res.data
}
