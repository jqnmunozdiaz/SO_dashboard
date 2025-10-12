import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { LayoutContainer, MainContent } from '@/components/Layout';
import Sidebar from '@/components/Sidebar';
import { FilterProvider } from '@/contexts/FilterContext';
import { TabProvider } from '@/contexts/TabContext';
import WelcomeModalProvider from '@/components/WelcomeModalProvider';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
});

export const metadata: Metadata = {
  title: 'World Bank Dashboard',
  description: 'World Bank project dashboard with filters and analytics',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} font-sans antialiased`}>
        <FilterProvider>
          <TabProvider>
            <LayoutContainer>
              <Sidebar />
              <MainContent>{children}</MainContent>
            </LayoutContainer>
            <WelcomeModalProvider>
              <div />
            </WelcomeModalProvider>
          </TabProvider>
        </FilterProvider>
      </body>
    </html>
  );
}
