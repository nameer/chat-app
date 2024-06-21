'use client'

import { SWRWrapper } from '@/lib/swr'
import { Box, Toolbar } from '@mui/material'
import Header from './Header'

export default function Layout({ children }: { children: React.ReactNode }) {
  const user = { name: 'npk', phoneNumber: '+919876543210' }
  return (
    <SWRWrapper>
      <Box sx={{ display: 'flex' }}>
        <Header user={user} />
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            p: 2,
          }}
        >
          <Toolbar />
          <Box
            sx={{
              minHeight: theme =>
                `calc(100vh - (${
                  theme.mixins.toolbar?.minHeight || 0
                }px + ${theme.spacing(5)}))`,
              overflow: 'auto',
            }}
          >
            {children}
          </Box>
        </Box>
      </Box>
    </SWRWrapper>
  )
}
