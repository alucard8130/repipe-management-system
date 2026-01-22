export default function AdminDashboard() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Admin Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded shadow">
          <p className="text-gray-500 text-sm">Active Projects</p>
          <p className="text-2xl font-bold">—</p>
        </div>

        <div className="bg-white p-4 rounded shadow">
          <p className="text-gray-500 text-sm">Pending Invoices</p>
          <p className="text-2xl font-bold">—</p>
        </div>

        <div className="bg-white p-4 rounded shadow">
          <p className="text-gray-500 text-sm">Low Stock Items</p>
          <p className="text-2xl font-bold">—</p>
        </div>
      </div>
    </div>
  )
}
