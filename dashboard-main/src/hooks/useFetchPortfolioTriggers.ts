import { useEffect, useState } from 'react';
import { PORTFOLIO_ENDPOINTS, fetchJson } from '@/api.settings';

export type PortfolioTriggerItem = {
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
  triggerText: string;
  additionalInfo: string;
  healthRelatedEmergencies: string;
  disastersTriggered: string;
  link: string;
};

type ResponseShape = { data: PortfolioTriggerItem[] };

export const useFetchPortfolioTriggers = () => {
  const [data, setData] = useState<PortfolioTriggerItem[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string>('');

  useEffect(() => {
    const abortController = new AbortController();
    const load = async () => {
      try {
        setIsLoading(true);
        const json = await fetchJson<ResponseShape>(
          PORTFOLIO_ENDPOINTS.triggers,
          { signal: abortController.signal }
        );
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
  }, []);

  return { data, isLoading, errorMessage };
};
