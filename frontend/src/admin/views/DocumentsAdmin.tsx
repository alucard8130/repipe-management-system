import { useEffect, useState } from "react"
import {
  fetchDocuments,
  uploadDocument,
  toggleVisibility,
} from "../../api/documents"

const CATEGORIES = [
  "CONTRACT",
  "PERMIT",
  "INSPECTION",
  "PHOTO",
  "INVOICE",
  "OTHER",
]

export default function DocumentsAdmin() {
  const [documents, setDocuments] = useState<any[]>([])
  const [file, setFile] = useState<File | null>(null)
  const [category, setCategory] = useState("CONTRACT")
  const [visible, setVisible] = useState(true)

  useEffect(() => {
    load()
  }, [])

  function load() {
    fetchDocuments().then(setDocuments)
  }

  async function handleUpload() {
    if (!file) return

    const form = new FormData()
    form.append("file", file)
    form.append("category", category)
    form.append("visible_to_client", String(visible))

    await uploadDocument(form)
    setFile(null)
    load()
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Documents</h1>

      {/* UPLOAD */}
      <div className="bg-white p-4 rounded shadow space-y-4">
        <h2 className="font-semibold">Upload Document</h2>

        <input
          type="file"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />

        <select
          className="border p-2 rounded"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          {CATEGORIES.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>

        <label className="flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            checked={visible}
            onChange={(e) => setVisible(e.target.checked)}
          />
          Visible to client
        </label>

        <button
          onClick={handleUpload}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Upload
        </button>
      </div>

      {/* LIST */}
      <div className="bg-white rounded shadow">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b text-left">
              <th className="p-3">Name</th>
              <th>Category</th>
              <th>Size</th>
              <th>Client</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {documents.map((d) => (
              <tr key={d.id} className="border-b">
                <td className="p-3">{d.file_name}</td>
                <td>{d.category}</td>
                <td>{(d.file_size / 1024).toFixed(1)} KB</td>
                <td>
                  <input
                    type="checkbox"
                    checked={d.visible_to_client}
                    onChange={() =>
                      toggleVisibility(d.id, !d.visible_to_client).then(load)
                    }
                  />
                </td>
                <td>
                  <a
                    href={`/api/documents/${d.id}/download/`}
                    className="text-blue-600 hover:underline"
                  >
                    Download
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
