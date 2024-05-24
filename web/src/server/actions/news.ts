'use server'

import { ApiResponse, PaginationApiResponse } from '@/@types'
import { INewsData, INewsDetail } from '@/@types/news'
import axiosClient from '@/lib/axios-client'

type GetNewsByCategoryProps = {
  pageParam?: number
  category?: string
}

export const getNewsByCategory = async ({ pageParam, category }: GetNewsByCategoryProps) => {
  const endpoint = category ? `/news/category/${category}` : '/news'

  const { data: response } = await axiosClient.get<PaginationApiResponse<INewsData[]>>(
    `${endpoint}?page=${pageParam}&&offset=20`
  )

  return response.data
}

export const getNewsBySlug = async (slug: string) => {
  const { data: response } = await axiosClient.get<ApiResponse<INewsDetail[]>>(`/news/${slug}`)

  return response.message[0]
}
