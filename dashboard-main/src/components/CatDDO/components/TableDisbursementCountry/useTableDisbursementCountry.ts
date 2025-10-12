import { useMemo } from 'react';
import type { DisbursementCountry } from '../../interfaces';
import { useFetchDisbursementsByCountry } from '@/hooks/useFetchDisbursementsByCountry';

export const useTableDisbursementCountry = () => {
  const { data, isLoading, error } = useFetchDisbursementsByCountry();

  const rawData = useMemo(() => data, [data]);

  const rows = useMemo<DisbursementCountry[]>(() => {
    if (!data.length) return [];

    const format = (n: number) =>
      n.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      });

    const dataRows: DisbursementCountry[] = data.map((item, index) => ({
      id: `${index + 1}`,
      country: item.country,
      netCommitmentAmount: format(item.netCommitment),
      cumulativeDisbursements: format(item.disbursements),
    }));

    // Calculate totals
    const totalNetCommitment = data.reduce(
      (sum, item) => sum + item.netCommitment,
      0
    );
    const totalDisbursements = data.reduce(
      (sum, item) => sum + item.disbursements,
      0
    );

    const totalRow: DisbursementCountry = {
      id: 'total',
      country: 'Grand Total',
      netCommitmentAmount: format(totalNetCommitment),
      cumulativeDisbursements: format(totalDisbursements),
      isTotal: true,
    };

    return [...dataRows, totalRow];
  }, [data]);

  return { rows, rawData, isLoading, errorMessage: error };
};
