import { BrowserRouter, Routes, Route } from "react-router-dom"
import Login from "./views/Login"
import Dashboard from "./views/Dashboard"
import Projects from "./views/Projects"
import Inventory from "./views/Inventory"
import ProtectedRoute from "./components/ProtectedRoute"

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
          <Route index element={<Projects />} />
          <Route path="projects" element={<Projects />} />
          <Route path="inventory" element={<Inventory />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
