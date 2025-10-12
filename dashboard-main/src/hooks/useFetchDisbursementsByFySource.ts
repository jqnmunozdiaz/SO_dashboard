import { useEffect, useState } from 'react';
import { PORTFOLIO_ENDPOINTS, fetchJson } from '@/api.settings';
import { useFilters } from '@/contexts/FilterContext';
import { buildApiUrl } from '@/lib/api-utils';

export interface DisbursementsByFySourceResponse {
  fiscalYears: string[];
  labels: string[];
  ibrd: number[];
  ida: number[];
  ibrdAndIda: number[];
  total: number[];
}

export const useFetchDisbursementsByFySource = () => {
  const { filters } = useFilters();
  const [data, setData] = useState<DisbursementsByFySourceResponse | null>(
    null
  );
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string>('');

  useEffect(() => {
    const abortController = new AbortController();
    const load = async () => {
      try {
        setIsLoading(true);

        const url = buildApiUrl(
          PORTFOLIO_ENDPOINTS.disbursementsByFySource,
          filters
        );

        const json = await fetchJson<DisbursementsByFySourceResponse>(url, {
          signal: abortController.signal,
        });
        setData(json);
        setErrorMessage('');
      } catch (err: unknown) {
        setData(null);
        setErrorMessage(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setIsLoading(false);
      }
    };
    load();
    return () => abortController.abort();
  }, [filters]);

  return { data, isLoading, errorMessage };
};
