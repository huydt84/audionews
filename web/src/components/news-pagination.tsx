import { PaginationData } from '@/@types'
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious
} from './ui/pagination'

type Props = {
  currentPage: number
  data: PaginationData
}

export default function NewsPagination({ currentPage, data }: Props) {
  return (
    <Pagination>
      <PaginationContent>
        <PaginationItem>
          <PaginationPrevious href="?page=1" isActive={currentPage === 1} />
        </PaginationItem>
        {Array.from(Array(data.totalPages))
          .slice(0, 3)
          .map((_, index) => (
            <PaginationItem key={index}>
              <PaginationLink href={`?page=${index + 1}`} isActive={currentPage === index + 1}>
                {index + 1}
              </PaginationLink>
            </PaginationItem>
          ))}
        {data.totalPages > 3 && (
          <PaginationItem>
            <PaginationEllipsis />
          </PaginationItem>
        )}
        <PaginationItem>
          <PaginationNext
            href={`?page=${data.totalPages}`}
            isActive={currentPage === data.totalPages}
          />
        </PaginationItem>
      </PaginationContent>
    </Pagination>
  )
}
