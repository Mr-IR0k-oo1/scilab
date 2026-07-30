import type { Metadata } from 'next';
import { Outfit } from 'next/font/google';
import './globals.css';
import '../styles.css';

const outfit = Outfit({ subsets: ['latin'], variable: '--font-outfit' });

export const metadata: Metadata = {
  title: 'FOSSEE Open Engineering Workspace',
  description: 'Free and Open Source Software in Education — a unified platform for simulation, modeling, and analysis.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className={outfit.variable}>{children}</body>
    </html>
  );
}
