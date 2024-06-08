import React from 'react'

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <section className="flex justify-center items-center w-full min-h-content">{children}</section>
  )
}
