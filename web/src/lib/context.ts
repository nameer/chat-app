import { PaletteMode } from '@mui/material'
import { createContext } from 'react'

export const ColorModeContext = createContext<{
  colorMode?: PaletteMode
  changeColorMode: (mode: PaletteMode | undefined) => void
}>({
  changeColorMode: (_: PaletteMode | undefined) => {},
})
