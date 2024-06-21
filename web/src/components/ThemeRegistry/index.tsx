'use client'

import * as React from 'react'

import CssBaseline from '@mui/material/CssBaseline'
import { ThemeProvider } from '@mui/material/styles'

import NextAppDirEmotionCacheProvider from './EmotionCache'
import { lightTheme, darkTheme } from './theme'
import { createTheme, PaletteMode } from '@mui/material'
import { ColorModeContext } from '@/lib/context'

const getDesignTokens = (mode: PaletteMode | undefined) => ({
  ...(getThemeMode(mode) === 'light' ? lightTheme : darkTheme),
})

const getThemeMode = (mode?: PaletteMode): PaletteMode => {
  let refinedMode = mode || localStorage.getItem('theme-mode')
  if (!refinedMode || (refinedMode !== 'dark' && refinedMode !== 'light'))
    refinedMode = window.matchMedia('(prefers-color-scheme: dark)')
      ? 'dark'
      : 'light'
  return refinedMode as PaletteMode
}

export default function ThemeRegistry({
  children,
}: {
  children: React.ReactNode
}) {
  const [mode, setMode] = React.useState<PaletteMode | undefined>(
    getThemeMode(),
  )
  const colorMode = React.useMemo(
    () => ({
      colorMode: mode,
      // The dark mode switch would invoke this method
      changeColorMode: (newMode: PaletteMode | undefined) => {
        if (newMode) localStorage.setItem('theme-mode', newMode)
        else localStorage.removeItem('theme-mode')
        setMode(newMode)
      },
    }),
    [mode],
  )

  // Update the theme only if the mode changes
  const theme = React.useMemo(() => createTheme(getDesignTokens(mode)), [mode])

  return (
    <NextAppDirEmotionCacheProvider options={{ key: 'mui' }}>
      <ColorModeContext.Provider value={colorMode}>
        <ThemeProvider theme={theme}>
          {/* CssBaseline kickstart an elegant, consistent, and simple baseline to build upon. */}
          <CssBaseline />
          {children}
        </ThemeProvider>
      </ColorModeContext.Provider>
    </NextAppDirEmotionCacheProvider>
  )
}
