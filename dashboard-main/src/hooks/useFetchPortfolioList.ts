import { useEffect, useState } from 'react';
import { PORTFOLIO_ENDPOINTS, fetchJson } from '@/api.settings';
import { useFilters } from '@/contexts/FilterContext';

export type PortfolioListItem = {
  id: string;
  projectId: string;
  country: string;
  projectName: string;
  fiscalYear: string;
  status: string;
  activationForCovid: string;
  financier: string;
  region: string;
  globalPractice: string;
  operationType: string;
};

type ResponseShape = { data: PortfolioListItem[] };

export const useFetchPortfolioList = () => {
  const { filters } = useFilters();
  const [data, setData] = useState<PortfolioListItem[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string>('');

  useEffect(() => {
    const abortController = new AbortController();
    const load = async () => {
      try {
        setIsLoading(true);

        // Build query parameters from filters
        const params = new URLSearchParams();
        if (filters.statuses.length) {
          params.append('statuses', filters.statuses.join(','));
        }
        if (filters.regions.length) {
          params.append('regions', filters.regions.join(','));
        }
        if (filters.countries.length) {
          params.append('countries', filters.countries.join(','));
        }

        const url = params.toString()
          ? `${PORTFOLIO_ENDPOINTS.list}?${params.toString()}`
          : PORTFOLIO_ENDPOINTS.list;

        const json = await fetchJson<ResponseShape>(url, {
          signal: abortController.signal,
        });
        setData(json.data ?? []);
        setErrorMessage('');
      } catch (err: unknown) {
        setData([]);
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
