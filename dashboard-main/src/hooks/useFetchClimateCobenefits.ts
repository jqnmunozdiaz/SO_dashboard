import { useState, useEffect } from 'react';
import { useFilters } from '@/contexts/FilterContext';
import { buildApiUrl } from '@/lib/api-utils';

interface ClimateCobenefitsResponse {
  standalone: {
    labels: string[];
    adapt: number[];
    mitig: number[];
    total: number[];
    avgTotal: number;
  };
  mixed: {
    labels: string[];
    adapt: number[];
    mitig: number[];
    total: number[];
    avgTotal: number;
  };
}

export function useFetchClimateCobenefits() {
  const { filters } = useFilters();
  const [data, setData] = useState<ClimateCobenefitsResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    async function fetchData() {
      try {
        setIsLoading(true);
        setError('');

        const url = buildApiUrl('/api/climate/cobenefits-bars', filters);
        const response = await fetch(url);

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result: ClimateCobenefitsResponse = await response.json();
        setData(result);
      } catch (err) {
        const message =
          err instanceof Error
            ? err.message
            : 'Failed to fetch climate cobenefits data';
        setError(message);
      } finally {
        setIsLoading(false);
      }
    }

    fetchData();
  }, [filters]);

  return { data, isLoading, error };
}
