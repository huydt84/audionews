'use client'

import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow
} from '@/components/ui/table'
import { useAdminGetAllNewsQuery } from '@/hooks/use-get-news-query'
import { formatTime } from '@/lib/data-time'
import Image from 'next/image'
import { Button } from './ui/button'
import { PlayIcon, Trash2Icon } from 'lucide-react'
import NewsPagination from './news-pagination'
import DeleteNewsButton from './delete-news-button'
import { useTransition } from 'react'
import { adminRegenerateNews } from '@/server/actions/news'
import { useToast } from './ui/use-toast'
import Link from 'next/link'

type Props = {
  currentPage: number
}

export function NewsTable({ currentPage }: Props) {
  const [isPending, startTransition] = useTransition()
  const { data } = useAdminGetAllNewsQuery()
  const { toast } = useToast()

  const onGenerateAudio = (newsId: number) => {
    startTransition(async () => {
      await adminRegenerateNews(newsId)

      toast({
        title: `Bắt đầu tạo audio cho bài viết ${newsId}.`
      })
    })
  }

  if (!data) return <p>Loading...</p>

  return (
    <>
      <Table>
        <TableCaption>Danh sách bài báo đã crawl.</TableCaption>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[100px]">Id</TableHead>
            <TableHead>Tiêu đề</TableHead>
            <TableHead>Nguồn</TableHead>
            <TableHead className="text-right">Thời điểm tạo</TableHead>
            <TableHead></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.data.map(news => (
            <TableRow key={news.id}>
              <TableCell className="font-medium">{news.id}</TableCell>
              <TableCell>
                <Link
                  href={`/news/${news.slug_url}`}
                  className="transition-all duration-200 hover:underline"
                >
                  {news.title}
                </Link>
              </TableCell>
              <TableCell>
                <Image
                  src={news.logo_url}
                  alt={news.title}
                  width={1280}
                  height={720}
                  className="w-[10rem] rounded-md"
                />
              </TableCell>
              <TableCell className="text-right">{formatTime(news.written_at)}</TableCell>
              <TableCell>
                <div className="flex justify-center items-center gap-4">
                  <DeleteNewsButton newsId={news.id} />

                  <Button variant="ghost" onClick={() => onGenerateAudio(news.id)}>
                    <PlayIcon className="text-green-600" />
                  </Button>
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <NewsPagination currentPage={currentPage} data={data.pagination} />
    </>
  )
}
