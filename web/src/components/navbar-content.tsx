'use client'

import Link from 'next/link'
import { usePathname, useRouter } from 'next/navigation'
import { Button } from './ui/button'
import { logout } from '@/server/actions/login'
import { useToast } from './ui/use-toast'
import { LogOutIcon } from 'lucide-react'

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

function UserNavbar() {
  return (
    <div className="flex justify-center items-center space-x-6 ml-8">
      <NavLink title="Tin mới nhất" url="/news" />

      <NavLink title="Thể thao" url="/sport" />

      <NavLink title="Thế giới" url="/world" />

      <NavLink title="Giáo dục" url="/education" />
    </div>
  )
}

type AdminNavbarProps = {
  username?: string
}

function AdminNavbar({ username }: AdminNavbarProps) {
  const router = useRouter()
  const { toast } = useToast()

  const onLogout = async () => {
    try {
      await logout()

      toast({
        title: 'Logout successfully'
      })
      router.push('/')
    } catch (error) {
      console.error(error)
    }
  }

  if (!username) return null

  return (
    <div className="flex justify-end items-center space-x-6 ml-8">
      <p>
        Đăng nhập dưới tên: <span className="font-medium">{username}</span>
      </p>
      <Button
        variant="link"
        onClick={onLogout}
        className="flex justify-center items-center gap-2 group"
      >
        <LogOutIcon className="w-4 h-4 ml-2 group-hover:translate-x-[-3px] transition-transform duration-150" />
        <span>Đăng xuất</span>
      </Button>
    </div>
  )
}

type Props = {
  user: { username: string } | null
}

export default function NavbarContent({ user }: Props) {
  const pathname = usePathname()

  const isAdminPage = pathname.startsWith('/admin')

  return (
    <nav className="px-6 py-4 bg-white sticky w-full z-20 top-0 start-0 border-b border-gray-200 flex gap-4 items-center">
      <Link href="/" className="text-2xl font-semibold">
        AudioNews
      </Link>

      {isAdminPage ? <AdminNavbar username={user?.username} /> : <UserNavbar />}
    </nav>
  )
}
