import { useEffect, useState } from 'react';
import { PORTFOLIO_ENDPOINTS, fetchJson } from '@/api.settings';
import { useFilters } from '@/contexts/FilterContext';
import { buildApiUrl } from '@/lib/api-utils';

export interface SummaryTableResponse {
  table: {
    IBRD: { Disbursed: number; Undisbursed: number; Pipeline: number };
    IDA: { Disbursed: number; Undisbursed: number; Pipeline: number };
  };
  Total: { Disbursed: number; Undisbursed: number; Pipeline: number };
}

export const useFetchSummaryTable = () => {
  const { filters } = useFilters();
  const [data, setData] = useState<SummaryTableResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string>('');

  useEffect(() => {
    const abortController = new AbortController();
    const load = async () => {
      try {
        setIsLoading(true);

        const url = buildApiUrl(PORTFOLIO_ENDPOINTS.summaryTable, filters);

        const json = await fetchJson<SummaryTableResponse>(url, {
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
