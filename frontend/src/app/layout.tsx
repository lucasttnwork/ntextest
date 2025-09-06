import type { Metadata } from "next";
import "./globals.css";
import { ThemeProvider } from "@/lib/theme-provider";

export const metadata: Metadata = {
  title: "NTEX - Gary Bencivenga Agent",
  description: "Sistema de IA para copywriting com Gary Bencivenga Agent",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-BR">
      <body className="antialiased font-sans" suppressHydrationWarning={true}>
        <ThemeProvider defaultTheme="dark" storageKey="ntex-ui-theme">
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
