'use server'
import axiosClient from '@/lib/axios-client'
import { LoginResponse } from '@/@types/auth'
import { cookies } from 'next/headers'
import * as z from 'zod'
import { ChangePasswordSchema } from '@/schema/login'

export const login = async (data: FormData) => {
  try {
    const { data: response } = await axiosClient.post<LoginResponse>('/login', data)

    cookies().set('token', response.access_token)

    return response.access_token
  } catch (error) {
    return { error: 'Login failed' }
  }
}

export const logout = async () => {
  try {
    cookies().set('token', '', {
      expires: new Date(0)
    })

    return true
  } catch (error) {
    return false
  }
}

export const getCurrentUser = async () => {
  try {
    const token = cookies().get('token')

    const { data: response } = await axiosClient.get<{ username: string }>('/me', {
      headers: {
        Authorization: `Bearer ${token?.value}`
      }
    })

    return response
  } catch (error) {
    return null
  }
}

export const changePassword = async (data: z.infer<typeof ChangePasswordSchema>) => {
  try {
    const token = cookies().get('token')

    const { data: response } = await axiosClient.post<{ success: boolean; message: string }>(
      '/change-password',
      data,
      {
        headers: {
          Authorization: `Bearer ${token?.value}`
        }
      }
    )

    if (response.success) {
      cookies().set('token', '', {
        expires: new Date(0)
      })
    }

    return response.success
  } catch (error) {
    return null
  }
}
