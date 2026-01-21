import { useState } from "react"
import { clientLogin } from "../api/clientPortal"
import { useNavigate } from "react-router-dom"

export default function ClientLogin() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const navigate = useNavigate()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    try {
      await clientLogin(email, password)
      navigate("/client/dashboard")
    } catch {
      setError("Invalid credentials")
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-800">
      <form className="bg-white p-6 rounded w-80 space-y-4" onSubmit={handleSubmit}>
        <h1 className="font-bold text-center">Client Login</h1>

        {error && <p className="text-red-600 text-sm">{error}</p>}

        <input
          type="email"
          placeholder="Email"
          className="w-full border p-2 rounded"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full border p-2 rounded"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button className="w-full bg-blue-600 text-white p-2 rounded">
          Login
        </button>
      </form>
    </div>
  )
}
