import { useState, useEffect } from 'react';

type FilterData = {
  regions: string[];
  countries: string[];
  statuses: string[];
  pillars: string[];
};

type UseFetchFiltersReturn = {
  filterData: FilterData | null;
  isLoading: boolean;
  error: string | null;
};

export function useFetchFilters(): UseFetchFiltersReturn {
  const [filterData, setFilterData] = useState<FilterData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchFilters() {
      try {
        setIsLoading(true);
        setError(null);

        const response = await fetch('/api/filters');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        if (result.error) {
          throw new Error(result.error);
        }

        setFilterData(result.data);
      } catch (err) {
        const message =
          err instanceof Error ? err.message : 'Failed to fetch filters';
        setError(message);
      } finally {
        setIsLoading(false);
      }
    }

    fetchFilters();
  }, []);

  return { filterData, isLoading, error };
}
