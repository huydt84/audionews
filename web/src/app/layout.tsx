import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { cn } from '@/lib/utils'
import Providers from '@/components/provider'
import { Toaster } from '@/components/ui/toaster'
import Navbar from '@/components/navbar'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'News',
  description: 'Audio news for busy people'
}

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body
        className={cn('w-screen h-screen relative overflow-x-hidden bg-[#edf2f7]', inter.className)}
      >
        <Navbar />

        <div className="min-h-content">
          <Providers>{children}</Providers>
        </div>

        <Toaster />
      </body>
    </html>
  )
}
