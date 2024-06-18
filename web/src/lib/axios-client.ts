import axios from 'axios'
import { cookies } from 'next/headers'

const axiosClient = axios.create({
  baseURL: process.env.API_URL,
  headers: {
    Accept: '*/*',
    'Access-Control-Allow-Origin': '*'
  },
  responseType: 'json'
})

axiosClient.interceptors.response.use(
  response => {
    return response
  },
  async error => {
    if (error?.response?.status === 401) {
      cookies().set('token', '', {
        expires: new Date(0)
      })

      return Promise.reject({ error: 'Unauthorized' })
    }

    return Promise.reject(error)
  }
)

export default axiosClient
