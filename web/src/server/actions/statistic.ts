'use server'

import { IApiResponse } from '@/@types'
import { IStatisticData } from '@/@types/news'
import axiosClient from '@/lib/axios-client'
import { cookies } from 'next/headers'

export const getAllTimeStatistic = async () => {
  try {
    const token = cookies().get('token')

    const { data: response } = await axiosClient.get<IApiResponse<IStatisticData>>(
      '/api/statistic',
      {
        headers: {
          Authorization: `Bearer ${token?.value}`
        }
      }
    )

    return response.data
  } catch (error) {
    return null
  }
}

export const getLatestStatistic = async () => {
  try {
    const token = cookies().get('token')

    const { data: response } = await axiosClient.get<IApiResponse<IStatisticData>>(
      '/api/statistic/last',
      {
        headers: {
          Authorization: `Bearer ${token?.value}`
        }
      }
    )

    return response.data
  } catch (error) {
    return null
  }
}
