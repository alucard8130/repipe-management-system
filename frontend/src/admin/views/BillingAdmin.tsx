import { useEffect, useState } from "react"
import { fetchInvoices, createInvoice } from "../../api/billing"
import { Link } from "react-router-dom"

export default function BillingAdmin() {
  const [invoices, setInvoices] = useState<any[]>([])
  const [projectId, setProjectId] = useState("")
  const [total, setTotal] = useState("")
  const [dueDate, setDueDate] = useState("")

  useEffect(() => {
    load()
  }, [])

  function load() {
    fetchInvoices().then(setInvoices)
  }

  async function handleCreate() {
    await createInvoice({
      project_id: Number(projectId),
      total,
      due_date: dueDate,
    })
    setProjectId("")
    setTotal("")
    setDueDate("")
    load()
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Billing</h1>

      {/* CREATE INVOICE */}
      <div className="bg-white p-4 rounded shadow space-y-3">
        <h2 className="font-semibold">New Invoice</h2>

        <input
          className="border p-2 rounded w-full"
          placeholder="Project ID"
          value={projectId}
          onChange={(e) => setProjectId(e.target.value)}
        />

        <input
          className="border p-2 rounded w-full"
          placeholder="Total"
          value={total}
          onChange={(e) => setTotal(e.target.value)}
        />

        <input
          type="date"
          className="border p-2 rounded w-full"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
        />

        <button
          onClick={handleCreate}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Create Invoice
        </button>
      </div>

      {/* LIST */}
      <div className="bg-white rounded shadow">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b text-left">
              <th className="p-3">Invoice</th>
              <th>Status</th>
              <th>Total</th>
              <th>Balance</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {invoices.map((i) => (
              <tr key={i.id} className="border-b">
                <td className="p-3">{i.invoice_number}</td>
                <td>{i.status}</td>
                <td>${i.total}</td>
                <td
                  className={
                    Number(i.balance) > 0
                      ? "text-red-600 font-semibold"
                      : ""
                  }
                >
                  ${i.balance}
                </td>
                <td className="text-right">
                  <Link
                    to={`/admin/billing/${i.id}`}
                    className="text-blue-600 hover:underline"
                  >
                    Open
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
