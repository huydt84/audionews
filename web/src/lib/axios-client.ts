import axios from 'axios'

const axiosClient = axios.create({
  baseURL: process.env.API_URL,
  headers: {
    'Content-Type': 'application/json',
    Accept: '*/*',
    'Access-Control-Allow-Origin': '*'
  },
  responseType: 'json'
})

export default axiosClient
