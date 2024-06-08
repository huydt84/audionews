import { adminGetNews, getNewsByCategory } from '@/server/actions/news'
import { useInfiniteQuery, useQuery } from '@tanstack/react-query'

export const useGetAllNewsQuery = (category?: string, searchValue?: string) =>
  useInfiniteQuery({
    queryKey: ['news', category, searchValue],
    queryFn: async ({ pageParam = 1 }) => getNewsByCategory({ pageParam, category }),
    getNextPageParam: (lastPage, allPages) => (lastPage.length ? allPages.length + 1 : undefined),
    initialPageParam: 1
  })

export const useAdminGetAllNewsQuery = (page?: number) =>
  useQuery({
    queryKey: ['news', page],
    queryFn: async () => adminGetNews({ pageParam: page })
  })
