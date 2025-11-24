'use client';

import { useAuth } from '@clerk/nextjs';
import { useEffect } from 'react';
import { apiClient } from '@/lib/api';

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const { getToken } = useAuth();

  useEffect(() => {
    // Set the token getter function for the API client
    apiClient.setTokenGetter(getToken);
  }, [getToken]);

  return <>{children}</>;
}
