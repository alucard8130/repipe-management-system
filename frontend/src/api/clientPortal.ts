import api from "./client"

export async function clientLogin(email: string, password: string) {
  const res = await api.post("/client/auth/login/", { email, password })
  localStorage.setItem("client_token", res.data.access)
  return res.data
}

export async function fetchClientProject(token: string) {
  const res = await api.get(`/client/project/${token}/`)
  return res.data
}
