import { useMemo } from 'react';
import type { PriorAction } from '../../interfaces';
import { useFetchPriorActions } from '@/hooks/useFetchPriorActions';

export function useTablePriorActions() {
  const { tableData, isLoading, error } = useFetchPriorActions();

  const rows = useMemo((): PriorAction[] => {
    if (!tableData?.length) return [];

    return tableData.map((row, index) => ({
      id: `${index + 1}`,
      projectNumber: row['P#'] ?? '',
      country: row['Country'] ?? '',
      drmPillar: row['DRM Pillar'] ?? '',
      priorAction: row['Prior Action'] ?? '',
      resultIndicator: row['Result Indicator'] ?? '',
      isTotal: false,
    }));
  }, [tableData]);

  return {
    rows,
    isLoading,
    errorMessage: error,
  };
}
