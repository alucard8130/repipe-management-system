import api from "./client"

export async function fetchInvoices() {
  const res = await api.get("/billing/invoices/")
  return res.data.results
}

export async function fetchInvoice(id: number) {
  const res = await api.get(`/billing/invoices/${id}/`)
  return res.data
}

export async function createPayment(payload: {
  invoice_id: number
  amount: string
  method: string
  reference?: string
  notes?: string
}) {
  const res = await api.post("/billing/payments/", payload)
  return res.data
}
