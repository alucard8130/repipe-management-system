import type { JSX } from "react";

export default function ClientLayout({ children }: { children: JSX.Element }) {
  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow p-4 font-bold">
        Project Status
      </header>
      <main className="p-4">{children}</main>
    </div>
  )
}
