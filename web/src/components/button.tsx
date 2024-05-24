import { cn } from '@/lib/utils'

interface Props extends React.ButtonHTMLAttributes<HTMLButtonElement> {}

export default function Button({ className, ...props }: Props) {
  return <button className={cn('', className)} {...props} />
}
