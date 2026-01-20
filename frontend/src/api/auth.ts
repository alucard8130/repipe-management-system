

import api from "./client"

export async function login(email: string, password: string) {
  const res = await api.post("/auth/token/", { email, password })

  const { access, refresh } = res.data
  localStorage.setItem("access_token", access)
  localStorage.setItem("refresh_token", refresh)

  return res.data
}

export function logout() {
  localStorage.removeItem("access_token")
  localStorage.removeItem("refresh_token")
}

export function isAuthenticated(): boolean {
  return Boolean(localStorage.getItem("access_token"))
}
