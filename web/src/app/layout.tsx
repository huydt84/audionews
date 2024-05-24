import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Navbar from '@/components/navbar'
import { cn } from '@/lib/utils'
import Providers from '@/components/provider'

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
        className={cn('w-screen h-full relative overflow-x-hidden bg-[#edf2f7]', inter.className)}
      >
        <Navbar />

        <div className="p-12 max-w-[1800px] mx-auto">
          <Providers>{children}</Providers>
        </div>
      </body>
    </html>
  )
}
