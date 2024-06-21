import { fetcher } from '@/services/api'
import { SWRConfig } from 'swr'

export const SWRWrapper = ({ children }: { children: React.ReactNode }) => (
  <SWRConfig value={{ fetcher }}>{children}</SWRConfig>
)
