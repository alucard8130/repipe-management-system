import { Outlet, useNavigate } from "react-router-dom"
import { logout } from "../api/auth"

export default function Dashboard() {
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate("/login")
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow p-4 flex justify-between">
        <span className="font-bold">Repipe System</span>
        <button
          onClick={handleLogout}
          className="text-red-600 hover:underline"
        >
          Logout
        </button>
      </header>

      <main className="p-4">
        <Outlet />
      </main>
    </div>
  )
}
