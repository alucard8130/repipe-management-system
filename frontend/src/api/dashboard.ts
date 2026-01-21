import api from "./client"

export async function fetchProjects() {
  const res = await api.get("/projects/")
  return res.data.results
}
