// src/app/layout.tsx
'use client';

import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import React, { useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';

const inter = Inter({ subsets: ['latin'] });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  
  const router = useRouter(); // Initialize the router

  useEffect(() => {
    if (typeof window !== 'undefined' && router.pathname === '/') {
      router.push('/ai'); // Redirect to the AI page
    }
  }, [router.pathname]);

  return (
    <html lang="en">
      <body className={inter.className}>
        <div>
          <nav className="mb-2"> {/* Adjust margin here */}
            <ul>
              <li><Link href="/ai">AI Assistant</Link></li>
              <li><Link href="/todo">Todo List</Link></li>
              <li><Link href="/game">Game</Link></li>
            </ul>
          </nav>
          <main>{children}</main>
        </div>
      </body>
    </html>
  );
}