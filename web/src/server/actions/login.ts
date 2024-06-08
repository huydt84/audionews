'use server'
import axiosClient from '@/lib/axios-client'
import { LoginResponse } from '@/@types/auth'
import { cookies } from 'next/headers'

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
