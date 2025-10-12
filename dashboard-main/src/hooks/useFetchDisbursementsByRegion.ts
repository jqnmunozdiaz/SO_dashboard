import { useState, useEffect } from 'react';
import { useFilters } from '@/contexts/FilterContext';
import { buildApiUrl } from '@/lib/api-utils';

interface DisbursementRegionData {
  region: string;
  netCommitment: number;
  disbursements: number;
  rawNetCommitment: number;
  rawDisbursements: number;
}

interface DisbursementsByRegionResponse {
  regions: DisbursementRegionData[];
}

export const useFetchDisbursementsByRegion = () => {
  const { filters } = useFilters();
  const [data, setData] = useState<DisbursementRegionData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        setError(null);

        const url = buildApiUrl(
          '/api/portfolio/disbursements-by-region',
          filters
        );
        const response = await fetch(url);

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result: DisbursementsByRegionResponse = await response.json();
        setData(result.regions);
      } catch (err) {
        const message =
          err instanceof Error
            ? err.message
            : 'Failed to fetch disbursements by region';
        setError(message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [filters]);

  return { data, isLoading, error };
};
