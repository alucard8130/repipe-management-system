import { useEffect, useState } from "react"
import { fetchInvoices } from "../api/billing"
import PaymentModal from "../components/PaymentModal"

type Invoice = {
  id: number
  invoice_number: string
  status: string
  total: string
  balance: string
  issue_date: string
}

export default function Billing() {
  const [invoices, setInvoices] = useState<Invoice[]>([])
  const [selected, setSelected] = useState<Invoice | null>(null)

  useEffect(() => {
    fetchInvoices().then(setInvoices)
  }, [])

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Billing</h1>

      <div className="bg-white rounded shadow p-4">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b text-left">
              <th>Invoice</th>
              <th>Status</th>
              <th>Total</th>
              <th>Balance</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {invoices.map((inv) => (
              <tr key={inv.id} className="border-b">
                <td className="py-2">{inv.invoice_number}</td>
                <td>{inv.status}</td>
                <td>${inv.total}</td>
                <td
                  className={
                    Number(inv.balance) > 0 ? "text-red-600 font-semibold" : ""
                  }
                >
                  ${inv.balance}
                </td>
                <td>
                  <button
                    className="text-blue-600 hover:underline"
                    onClick={() => setSelected(inv)}
                  >
                    Pay
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selected && (
        <PaymentModal
          invoice={selected}
          onClose={() => setSelected(null)}
          onSuccess={() => {
            setSelected(null)
            fetchInvoices().then(setInvoices)
          }}
        />
      )}
    </div>
  )
}
