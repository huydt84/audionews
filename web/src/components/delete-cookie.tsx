'use client'

import { useEffect } from 'react'
import Cookies from 'js-cookie'
import { useRouter } from 'next/navigation'

export default function DeleteCookie() {
  const router = useRouter()

  const handleDeleteCookies = () => {
    Cookies.remove('token')
    router.replace('/admin/login')
  }

  useEffect(() => {
    handleDeleteCookies()
  }, [])

  return <p>Please login again</p>
}
