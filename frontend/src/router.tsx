import { BrowserRouter, Routes, Route } from "react-router-dom"
import Login from "./views/Login"
import Dashboard from "./views/Dashboard"
import Projects from "./views/Projects"
import Inventory from "./views/Inventory"
import ProtectedRoute from "./components/ProtectedRoute"
import DashboardHome from "./views/DashboardHome"
import Billing from "./views/Billing"
import Kardex from "./views/Kardex"
import ClientLogin from "./client/ClientLogin"
import ClientLayout from "./client/ClientLayout"
import ClientProject from "./client/ClientProject"
import AdminLayout from "./admin/layout/AdminLayout"
import AdminDashboard from "./admin/views/AdminDashboard"
import ProjectsAdmin from "./admin/views/ProjectsAdmin"
import ProjectDetail from "./admin/views/ProjectDetail"
import DocumentsAdmin from "./admin/views/DocumentsAdmin"
import ClientAccessDetail from "./admin/views/ClientAccessDetail"
import ClientsAdmin from "./admin/views/ClientsAdmin"
import InvoiceDetail from "./admin/views/InvoiceDetail"
import BillingAdmin from "./admin/views/BillingAdmin"

export default function Router() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route path="/"element={<ProtectedRoute><Dashboard /></ProtectedRoute>}>
          <Route index element={<DashboardHome />} />
          <Route path="projects" element={<Projects />} />
          <Route path="inventory" element={<Inventory />} />
          <Route path="billing" element={<Billing />} />
          <Route path="kardex" element={<Kardex />} />
          <Route path="/client/login" element={<ClientLogin />} />
          <Route path="/client">
  <Route index element={<ClientLogin />} />
  <Route path="project/:token" element={<ClientProject />} />
  <Route
    path="dashboard"
    element={
      <ClientLayout>
        <ClientProject />
      </ClientLayout>
    }
  />
</Route>
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
<Route
  path="/admin"
  element={
    <ProtectedRoute>
      <AdminLayout />
    </ProtectedRoute>
  }
>
  <Route index element={<AdminDashboard />} />
  <Route path="projects" element={<ProjectsAdmin />} />
  <Route path="/admin/projects/:id" element={<ProjectDetail />} />
  <Route path="/admin/documents" element={<DocumentsAdmin />} />
  <Route path="/admin/clients" element={<ClientsAdmin />} />
  <Route path="/admin/clients/:id" element={<ClientAccessDetail />} />
  <Route path="/admin/billing" element={<BillingAdmin />} />
  <Route path="/admin/billing/:invoiceId" element={<InvoiceDetail />} />
</Route>



