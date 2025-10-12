import { useMemo } from 'react';
import type { DisbursementRegion } from '../../interfaces';
import { useFetchDisbursementsByRegion } from '@/hooks/useFetchDisbursementsByRegion';

export const useTableDisbursementRegion = () => {
  const { data, isLoading, error } = useFetchDisbursementsByRegion();

  const rawData = useMemo(() => data, [data]);

  const rows = useMemo<DisbursementRegion[]>(() => {
    if (!data.length) return [];

    const format = (n: number) =>
      n.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      });

    const dataRows: DisbursementRegion[] = data.map((item, index) => ({
      id: `${index + 1}`,
      region: item.region,
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

    const totalRow: DisbursementRegion = {
      id: 'total',
      region: 'Grand Total',
      netCommitmentAmount: format(totalNetCommitment),
      cumulativeDisbursements: format(totalDisbursements),
      isTotal: true,
    };

    return [...dataRows, totalRow];
  }, [data]);

  return { rows, rawData, isLoading, errorMessage: error };
};
