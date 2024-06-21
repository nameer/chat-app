import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import ThemeRegistry from '../components/ThemeRegistry'
import Main from '@/components/Main'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: process.env.NEXT_PUBLIC_PROJECT_NAME,
  description: process.env.NEXT_PUBLIC_PROJECT_DESCRIPTION,
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <head>
        <link
          rel="apple-touch-icon"
          sizes="180x180"
          href="/apple-touch-icon.png"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="32x32"
          href="/favicon-32x32.png"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="16x16"
          href="/favicon-16x16.png"
        />
        <link rel="manifest" href="/site.webmanifest" />
        <link rel="mask-icon" href="/safari-pinned-tab.svg" color="#5bbad5" />
        <meta name="msapplication-TileColor" content="#da532c" />
        <meta
          name="theme-color"
          content="#138a72"
          media="(prefers-color-scheme: light)"
        />
        <meta
          name="theme-color"
          content="#0d6755"
          media="(prefers-color-scheme: dark)"
        />
      </head>
      <body className={inter.className}>
        <ThemeRegistry>
          <Main>{children}</Main>
        </ThemeRegistry>
      </body>
    </html>
  )
}
