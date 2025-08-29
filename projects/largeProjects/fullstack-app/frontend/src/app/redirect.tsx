// src/app/Redirect.tsx
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/router';

const Redirect = () => {
  const router = useRouter();

  useEffect(() => {
    if (router.pathname === '/') {
      router.push('/ai'); // Redirect to the AI page
    }
  }, [router]);

  return null; // This component does not render anything
};

export default Redirect;