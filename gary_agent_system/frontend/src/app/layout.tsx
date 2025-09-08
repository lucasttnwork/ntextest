import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Gary Bencivenga Chat',
  description: 'Interface de chat com o Agente Gary Bencivenga - Copywriting Mestre',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="pt-BR">
      <body className="bg-gray-50">
        <div className="min-h-screen bg-gradient-to-br from-amber-50 to-orange-100">
          {children}
        </div>
      </body>
    </html>
  )
}