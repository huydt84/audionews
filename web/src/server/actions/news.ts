'use server'

import { ApiResponse, PaginationApiResponse } from '@/@types'
import { INewsData, INewsDetail } from '@/@types/news'
import axiosClient from '@/lib/axios-client'
import { cookies } from 'next/headers'

type GetNewsByCategoryProps = {
  pageParam?: number
  category?: string
}

export const getNewsByCategory = async ({ pageParam = 1, category }: GetNewsByCategoryProps) => {
  const endpoint = category ? `/api/news/category/${category}` : '/api/news'

  const { data: response } = await axiosClient.get<PaginationApiResponse<INewsData[]>>(
    `${endpoint}?page=${pageParam}&&offset=20`
  )

  return response.data
}

export const getNewsBySlug = async (slug: string) => {
  const { data: response } = await axiosClient.get<ApiResponse<INewsDetail[]>>(`/api/news/${slug}`)

  return response.message[0]
}

export const adminGetNews = async ({ pageParam = 1 }: GetNewsByCategoryProps) => {
  const { data: response } = await axiosClient.get<PaginationApiResponse<INewsData[]>>(
    `/api/news?page=${pageParam}&&offset=20`
  )

  return response
}

export const adminDeleteNews = async (newsId: number) => {
  try {
    const token = cookies().get('token')?.value

    const { data: response } = await axiosClient.delete<ApiResponse<null>>(`/api/news/${newsId}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    return response
  } catch (error) {
    return null
  }
}

export const adminRegenerateNews = async (newsId: number) => {
  try {
    const token = cookies().get('token')?.value

    const { data: response } = await axiosClient.get<ApiResponse<null>>(
      `/api/news/generate-audio/${newsId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )

    return response
  } catch (error) {
    return null
  }
}
