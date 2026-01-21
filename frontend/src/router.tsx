import { BrowserRouter, Routes, Route } from "react-router-dom"
import Login from "./views/Login"
import Dashboard from "./views/Dashboard"
import Projects from "./views/Projects"
import Inventory from "./views/Inventory"
import ProtectedRoute from "./components/ProtectedRoute"
import DashboardHome from "./views/DashboardHome"
import Billing from "./views/Billing"
import Kardex from "./views/Kardex"

export default function Router() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        >
          <Route index element={<DashboardHome />} />
          <Route path="projects" element={<Projects />} />
          <Route path="inventory" element={<Inventory />} />
          <Route path="billing" element={<Billing />} />
          <Route path="kardex" element={<Kardex />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
