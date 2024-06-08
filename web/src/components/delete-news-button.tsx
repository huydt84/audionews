import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger
} from '@/components/ui/alert-dialog'
import { Button } from '@/components/ui/button'
import { adminDeleteNews } from '@/server/actions/news'
import { Trash2Icon } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { useTransition } from 'react'
import { useToast } from './ui/use-toast'

type Props = {
  newsId: number
}

export default function DeleteNewsButton({ newsId }: Props) {
  const [isPending, startTransition] = useTransition()
  const router = useRouter()
  const { toast } = useToast()

  const onDelete = () => {
    startTransition(async () => {
      await adminDeleteNews(newsId)

      toast({
        title: 'Xóa bài viết thành công'
      })
      window.location.reload()
    })
  }

  return (
    <AlertDialog>
      <AlertDialogTrigger asChild>
        <Button variant="ghost">
          <Trash2Icon className="text-red-600" />
        </Button>
      </AlertDialogTrigger>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Bạn có chắc chắn muốn xóa bài viết này?</AlertDialogTitle>
          <AlertDialogDescription>
            Với thao tác này bài viết của bạn sẽ bị xóa hoàn toàn khỏi cơ sở dữ liệu và sẽ không thể
            khôi phục được.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Hủy</AlertDialogCancel>
          <AlertDialogAction onClick={onDelete} disabled={isPending}>
            {isPending ? 'Đang xóa...' : 'Tiếp tục'}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}
