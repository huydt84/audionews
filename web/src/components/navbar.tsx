'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

type NavLinkProps = {
  title: string
  url: string
}

function NavLink({ title, url }: NavLinkProps) {
  const pathname = usePathname()
  const isActive = pathname === url

  return (
    <Link
      href={url}
      className="relative font-medium hover:text-blue-700 transition-color duration-200"
    >
      {title}
      {isActive && (
        <div className="h-[3px] absolute bg-blue-700 w-full translate-y-[17px] rounded-full"></div>
      )}
    </Link>
  )
}

export default function Navbar() {
  return (
    <nav className="px-6 py-4 bg-white sticky w-full z-20 top-0 start-0 border-b border-gray-200 flex gap-4 items-center">
      <Link href="/" className="text-2xl font-semibold">
        AudioNews
      </Link>

      <div className="flex justify-center items-center space-x-6 ml-8">
        <NavLink title="Tin mới nhất" url="/news" />

        <NavLink title="Thể thao" url="/sport" />

        <NavLink title="Thế giới" url="/world" />

        <NavLink title="Giáo dục" url="/education" />
      </div>
    </nav>
  )
}
