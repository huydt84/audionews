import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

export const middleware = async (req: NextRequest) => {
  const { nextUrl } = req
  const token = cookies().get('token')?.value

  const isAdminPage = nextUrl.pathname === '/admin' || nextUrl.pathname === '/admin/change-password'
  const isLoginPage = nextUrl.pathname === '/admin/login'

  if (isAdminPage && !token) {
    return NextResponse.redirect(new URL('/admin/login', nextUrl))
  }

  if (isLoginPage && token) {
    return NextResponse.redirect(new URL('/admin', nextUrl))
  }
}

export const config = {
  matcher: ['/((?!.+\\.[\\w]+$|_next).*)', '/', '/(api|trpc)(.*)']
}
