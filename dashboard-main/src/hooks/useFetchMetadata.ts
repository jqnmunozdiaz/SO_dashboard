import { useState, useEffect } from 'react';
import type { Metadata } from '@/lib/portfolio';

interface MetadataResponse {
  data: Metadata;
}

export function useFetchMetadata() {
  const [metadata, setMetadata] = useState<Metadata>({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    async function fetchData() {
      try {
        setIsLoading(true);
        setError('');

        const response = await fetch('/api/metadata');

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result: MetadataResponse = await response.json();
        setMetadata(result.data);
      } catch (err) {
        const message =
          err instanceof Error ? err.message : 'Failed to fetch metadata';
        setError(message);
        console.error('Error fetching metadata:', err);
      } finally {
        setIsLoading(false);
      }
    }

    fetchData();
  }, []);

  return { metadata, isLoading, error };
}
