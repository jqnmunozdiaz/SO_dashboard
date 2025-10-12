import { useState, useEffect } from 'react';
import { useFilters } from '@/contexts/FilterContext';
import { buildApiUrl } from '@/lib/api-utils';

interface DisbursementCountryData {
  country: string;
  netCommitment: number;
  disbursements: number;
  rawNetCommitment: number;
  rawDisbursements: number;
}

interface DisbursementsByCountryResponse {
  countries: DisbursementCountryData[];
}

export const useFetchDisbursementsByCountry = () => {
  const { filters } = useFilters();
  const [data, setData] = useState<DisbursementCountryData[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        setError(null);

        const url = buildApiUrl(
          '/api/portfolio/disbursements-by-country',
          filters
        );
        const response = await fetch(url);

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result: DisbursementsByCountryResponse = await response.json();
        setData(result.countries);
      } catch (err) {
        const message =
          err instanceof Error
            ? err.message
            : 'Failed to fetch disbursements by country';
        setError(message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, [filters]);

  return { data, isLoading, error };
};
