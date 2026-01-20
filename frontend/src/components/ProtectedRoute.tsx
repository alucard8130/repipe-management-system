import { Navigate } from "react-router-dom"
import { isAuthenticated } from "../api/auth"
import type { JSX } from "react"

export default function ProtectedRoute({ children }: { children: JSX.Element }) {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />
  }
  return children
}

