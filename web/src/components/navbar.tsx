import { getCurrentUser } from '@/server/actions/login'
import NavbarContent from './navbar-content'

export default async function Navbar() {
  const user = await getCurrentUser()

  return <NavbarContent user={user} />
}
