import { useState } from "react"
import { createPayment } from "../api/billing"

type Props = {
  invoice: {
    id: number
    invoice_number: string
    balance: string
  }
  onClose: () => void
  onSuccess: () => void
}

export default function PaymentModal({ invoice, onClose, onSuccess }: Props) {
  const [amount, setAmount] = useState("")
  const [method, setMethod] = useState("CASH")
  const [error, setError] = useState("")

  async function handlePay() {
    if (!amount) return
    setError("")

    try {
      await createPayment({
        invoice_id: invoice.id,
        amount,
        method,
      })
      onSuccess()
    } catch (err: any) {
      setError(err.response?.data?.error || "Payment failed")
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center">
      <div className="bg-white p-6 rounded w-96 space-y-4">
        <h2 className="font-bold">
          Pay {invoice.invoice_number}
        </h2>

        <p className="text-sm text-gray-500">
          Balance: ${invoice.balance}
        </p>

        {error && <p className="text-red-600 text-sm">{error}</p>}

        <input
          type="number"
          placeholder="Amount"
          className="w-full border p-2 rounded"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />

        <select
          className="w-full border p-2 rounded"
          value={method}
          onChange={(e) => setMethod(e.target.value)}
        >
          <option value="CASH">Cash</option>
          <option value="CHECK">Check</option>
          <option value="ACH">ACH</option>
          <option value="ZELLE">Zelle</option>
          <option value="CARD">Card</option>
        </select>

        <div className="flex justify-end gap-2">
          <button onClick={onClose} className="border px-3 py-1 rounded">
            Cancel
          </button>
          <button
            onClick={handlePay}
            className="bg-green-600 text-white px-3 py-1 rounded"
          >
            Pay
          </button>
        </div>
      </div>
    </div>
  )
}
