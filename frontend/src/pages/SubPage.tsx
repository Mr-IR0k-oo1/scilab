'use client';

import { useEffect, type ReactNode } from 'react';

interface SubPageProps {
  title: string;
  children: ReactNode;
}

export default function SubPage({ title, children }: SubPageProps) {
  useEffect(() => {
    document.body.style.overflow = 'auto';
    document.documentElement.style.overflow = 'auto';
    return () => {
      document.body.style.overflow = '';
      document.documentElement.style.overflow = '';
    };
  }, []);

  return (
    <main className="overflow-x-hidden w-full max-w-full bg-background text-foreground min-h-screen font-sans">
      <div className="max-w-3xl mx-auto px-6 py-24">
        <a href="/" className="inline-flex items-center gap-2 text-xs text-muted-foreground/50 hover:text-foreground transition-colors mb-12 group">
          <span className="text-sm group-hover:-translate-x-1 transition-transform">&larr;</span>
          Back to FOSSEE
        </a>
        <h1 className="text-[clamp(2rem,3.5vw,3.5rem)] font-bold leading-[1.15] tracking-tight mb-6">{title}</h1>
        <div className="text-sm text-muted-foreground/70 leading-relaxed space-y-4">
          {children}
        </div>
      </div>
    </main>
  );
}
