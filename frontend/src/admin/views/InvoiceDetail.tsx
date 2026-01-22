import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { fetchInvoice, createPayment } from "../../api/billing"

export default function InvoiceDetail() {
  const { invoiceId } = useParams()
  const [invoice, setInvoice] = useState<any>(null)
  const [amount, setAmount] = useState("")
  const [method, setMethod] = useState("CASH")

  useEffect(() => {
    if (invoiceId) {
      fetchInvoice(Number(invoiceId)).then(setInvoice)
    }
  }, [invoiceId])

  async function handlePay() {
    await createPayment({
      invoice_id: invoice.id,
      amount,
      method,
    })
    setAmount("")
    fetchInvoice(invoice.id).then(setInvoice)
  }

  if (!invoice) return <p>Loading...</p>

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-bold">
        Invoice {invoice.invoice_number}
      </h1>

      <div className="bg-white p-4 rounded shadow space-y-2">
        <p>Status: <b>{invoice.status}</b></p>
        <p>Total: ${invoice.total}</p>
        <p>Balance: ${invoice.balance}</p>
      </div>

      {/* PAYMENTS */}
      <div className="bg-white p-4 rounded shadow space-y-3">
        <h2 className="font-semibold">Register Payment</h2>

        <input
          className="border p-2 rounded w-full"
          placeholder="Amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />

        <select
          className="border p-2 rounded w-full"
          value={method}
          onChange={(e) => setMethod(e.target.value)}
        >
          <option value="CASH">Cash</option>
          <option value="CHECK">Check</option>
          <option value="ACH">ACH</option>
          <option value="CARD">Card</option>
        </select>

        <button
          onClick={handlePay}
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          Pay
        </button>
      </div>

      {/* PAYMENT HISTORY */}
      <div className="bg-white rounded shadow p-4">
        <h2 className="font-semibold mb-2">Payments</h2>
        <ul className="space-y-1 text-sm">
          {invoice.payments.map((p: any) => (
            <li key={p.id}>
              {p.method} — ${p.amount} — {p.created_at}
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
