import { useEffect, useState } from "react"
import {
  fetchClients,
  createClient,
  toggleClient,
} from "../../api/clients"

export default function ClientsAdmin() {
  const [clients, setClients] = useState<any[]>([])
  const [email, setEmail] = useState("")
  const [name, setName] = useState("")

  useEffect(() => {
    load()
  }, [])

  function load() {
    fetchClients().then(setClients)
  }

  async function handleCreate() {
    await createClient({ email, name })
    setEmail("")
    setName("")
    load()
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Clients</h1>

      {/* CREATE */}
      <div className="bg-white p-4 rounded shadow space-y-3">
        <h2 className="font-semibold">New Client</h2>

        <input
          className="border p-2 rounded w-full"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          className="border p-2 rounded w-full"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <button
          onClick={handleCreate}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Create Client
        </button>
      </div>

      {/* LIST */}
      <div className="bg-white rounded shadow">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b text-left">
              <th className="p-3">Email</th>
              <th>Name</th>
              <th>Active</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {clients.map((c) => (
              <tr key={c.id} className="border-b">
                <td className="p-3">{c.email}</td>
                <td>{c.name}</td>
                <td>
                  <input
                    type="checkbox"
                    checked={c.is_active}
                    onChange={() =>
                      toggleClient(c.id, !c.is_active).then(load)
                    }
                  />
                </td>
                <td className="text-right">
                  <a
                    href={`/admin/clients/${c.id}`}
                    className="text-blue-600 hover:underline"
                  >
                    Access
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
