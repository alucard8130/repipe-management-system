import { NavLink } from "react-router-dom"

const links = [
  { to: "/admin", label: "Dashboard" },
  { to: "/admin/projects", label: "Projects" },
  { to: "/admin/documents", label: "Documents" },
  { to: "/admin/clients", label: "Clients" },
  { to: "/admin/inventory", label: "Inventory" },
  { to: "/admin/billing", label: "Billing" },
]

export default function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 text-white">
      <div className="p-4 font-bold text-lg border-b border-slate-700">
        Admin Panel
      </div>

      <nav className="p-4 space-y-2">
        {links.map((l) => (
          <NavLink
            key={l.to}
            to={l.to}
            className={({ isActive }) =>
              `block px-3 py-2 rounded ${
                isActive ? "bg-slate-700" : "hover:bg-slate-800"
              }`
            }
          >
            {l.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
