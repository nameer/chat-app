'use client'

import React, { useContext } from 'react'

import Image from 'next/image'
import { useRouter } from 'next/navigation'

import {
  AppBar,
  Avatar,
  Box,
  ClickAwayListener,
  IconButton,
  Menu,
  MenuItem,
  PaletteMode,
  Toolbar,
  Typography,
} from '@mui/material'

import { logout } from '@/services/api'
import { stringToColor } from '@/app/utils'
import {
  ContrastTwoTone,
  DarkModeTwoTone,
  LightModeTwoTone,
  LogoutTwoTone,
} from '@mui/icons-material'
import { ColorModeContext } from '@/lib/context'
import { UserType } from '@/models/user'

interface HeaderProps {
  user?: UserType
}

const Header: React.FC<HeaderProps> = ({ user }) => {
  const router = useRouter()

  const { colorMode, changeColorMode } = useContext(ColorModeContext)

  const [userMenuAnchorEl, setUserMenuAnchorEl] =
    React.useState<null | HTMLElement>(null)
  const userMenuOpen = Boolean(userMenuAnchorEl)

  const [themeMenuAnchorEl, setThemeMenuAnchorEl] =
    React.useState<null | HTMLElement>(null)
  const themeMenuOpen = Boolean(themeMenuAnchorEl)

  const handleLogout = () => {
    logout().then(() => {})
    router.push('/login')
  }

  const handleAvatarClick = (event: React.MouseEvent<HTMLElement>) =>
    setUserMenuAnchorEl(event.currentTarget)
  const handleThemeClick = (event: React.MouseEvent<HTMLElement>) =>
    setThemeMenuAnchorEl(event.currentTarget)

  const handleAvatarClickAway = () => setUserMenuAnchorEl(null)
  const handleThemeClickAway = () => setThemeMenuAnchorEl(null)

  const handleThemeChange = (mode: PaletteMode | undefined) => () =>
    changeColorMode(mode)

  const avatarBg = stringToColor(user?.name || '')

  return user ? (
    <AppBar
      position="fixed"
      color="default"
      sx={{ zIndex: theme => theme.zIndex.drawer + 1 }}
    >
      <Toolbar
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <Box display="flex" gap="3rem" alignItems="center">
          <IconButton aria-label="Logo" edge="start">
            <Image src="/icon.svg" width={24} height={24} alt="Logo" />
          </IconButton>
        </Box>
        <Box display="flex" gap="1.25rem" alignItems="center">
          <ClickAwayListener onClickAway={handleThemeClickAway}>
            <IconButton
              onClick={handleThemeClick}
              aria-controls={themeMenuOpen ? 'account-menu' : undefined}
              aria-haspopup="true"
              aria-expanded={themeMenuOpen ? 'true' : undefined}
            >
              {!colorMode ? (
                <ContrastTwoTone />
              ) : colorMode === 'dark' ? (
                <DarkModeTwoTone />
              ) : (
                <LightModeTwoTone />
              )}
            </IconButton>
          </ClickAwayListener>
          <ClickAwayListener onClickAway={handleAvatarClickAway}>
            <IconButton
              onClick={handleAvatarClick}
              size="small"
              aria-controls={userMenuOpen ? 'account-menu' : undefined}
              aria-haspopup="true"
              aria-expanded={userMenuOpen ? 'true' : undefined}
            >
              <Avatar
                alt={user.name}
                src={user.avatarUrl}
                sx={{
                  bgcolor: avatarBg,
                  cursor: 'pointer',
                  p: 1,
                }}
              >
                <Typography
                  color={theme => theme.palette.getContrastText(avatarBg)}
                >
                  {(user.name || '?')[0]}
                </Typography>
              </Avatar>
            </IconButton>
          </ClickAwayListener>
        </Box>

        <Menu
          anchorEl={userMenuAnchorEl}
          open={userMenuOpen}
          onClose={handleAvatarClickAway}
          onClick={handleAvatarClickAway}
          sx={{
            overflow: 'visible',
            width: 170,
          }}
          transformOrigin={{ horizontal: 'right', vertical: 'top' }}
          anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
        >
          <MenuItem disabled>
            <Typography sx={{ color: theme => theme.palette.text.primary }}>
              {user.name}
            </Typography>
          </MenuItem>
          <MenuItem onClick={handleLogout}>
            <LogoutTwoTone fontSize="small" sx={{ mr: 1 }} />
            Logout
          </MenuItem>
        </Menu>
        <Menu
          anchorEl={themeMenuAnchorEl}
          open={themeMenuOpen}
          onClose={handleThemeClickAway}
          onClick={handleThemeClickAway}
          sx={{
            overflow: 'visible',
            width: 170,
          }}
          transformOrigin={{ horizontal: 'right', vertical: 'top' }}
          anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
        >
          <MenuItem
            onClick={handleThemeChange(undefined)}
            selected={!colorMode}
          >
            <ContrastTwoTone fontSize="small" sx={{ mr: 1 }} />
            System
          </MenuItem>
          <MenuItem
            onClick={handleThemeChange('dark')}
            selected={colorMode === 'dark'}
          >
            <DarkModeTwoTone fontSize="small" sx={{ mr: 1 }} />
            Dark
          </MenuItem>
          <MenuItem
            onClick={handleThemeChange('light')}
            selected={colorMode === 'light'}
          >
            <LightModeTwoTone fontSize="small" sx={{ mr: 1 }} />
            Light
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  ) : (
    <></>
  )
}

export default Header
