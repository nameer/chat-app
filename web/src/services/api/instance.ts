import axios from 'axios'
import { camelizeKeys, decamelizeKeys } from 'humps'
import { deleteCookie } from 'cookies-next'
import { ACCESS_TOKEN_COOKIE } from '@/constants/auth'

const logout = async () => {
  try {
    await instance.post('/auth/revoke-token')
  } catch {}
  deleteCookie(ACCESS_TOKEN_COOKIE)
}

const createInstance = (baseURL: string) => {
  const axiosInstance = axios.create({
    baseURL,
    withCredentials: true,
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
  })

  // Request interceptor: camelCase to snake_case
  axiosInstance.interceptors.request.use(
    async config => {
      if (config.params) config.params = decamelizeKeys(config.params)
      if (config.data) config.data = decamelizeKeys(config.data)
      return config
    },
    async error => {
      if (error.response?.data)
        error.response.data = camelizeKeys(error.response.data)
      return Promise.reject(error)
    },
  )
  // Response interceptor: snake_case to camelCase
  axiosInstance.interceptors.response.use(
    async response => {
      return {
        ...response,
        data: camelizeKeys(response.data),
      }
    },
    async error => {
      if (error.response?.data)
        error.response.data = camelizeKeys(error.response.data)
      return Promise.reject(error)
    },
  )

  // Refresh the token(s) if expired.
  axiosInstance.interceptors.response.use(null, async error => {
    const originalRequest = error.config
    // Fail if the request is re-initiated one or status is not 'Unauthorized'.
    if (
      error.response?.status !== 401 ||
      originalRequest._retry ||
      originalRequest.url?.endsWith('/auth/refresh-token')
    ) {
      await logout()
      return Promise.reject(error)
    }

    try {
      // Refresh the tokens.
      const refreshInstance = createInstance(process.env.NEXT_PUBLIC_API_URL)
      await refreshInstance.post('/auth/refresh-token')
    } catch {
      // Refresh-token failure - redirect to login page.
      window.location.href = '/login'
      return Promise.reject(error)
    }
    // Re-initiate the request.
    originalRequest._retry = true
    return instance(originalRequest)
  })
  return axiosInstance
}

const instance = createInstance(process.env.NEXT_PUBLIC_API_URL)

export { createInstance, instance }
