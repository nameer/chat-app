import { logout, instance as api } from './axiosInstance'
import { AxiosRequestConfig } from 'axios'

const fetcher = (args: [string, AxiosRequestConfig?] | string) =>
  args instanceof Array
    ? api.get(...args).then(res => res.data)
    : api.get(args).then(res => res.data)

export { fetcher }

export { logout, api }
