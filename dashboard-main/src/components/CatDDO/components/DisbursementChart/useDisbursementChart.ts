import { useMemo } from 'react';
import type { StackedBarChartDataPoint } from '@/lib/BarChart';
import { disbursementSeries } from './constants/disbursementChartData';
import { useFetchDisbursementsByFySource } from '@/hooks/useFetchDisbursementsByFySource';

export const useDisbursementChart = () => {
  const { data, isLoading, errorMessage } = useFetchDisbursementsByFySource();

  const mappedData = useMemo<StackedBarChartDataPoint[]>(() => {
    if (
      !data?.fiscalYears?.length ||
      !data?.ibrd?.length ||
      !data?.ida?.length
    ) {
      return [];
    }

    return data.fiscalYears.map((year, index) => {
      const shortLabel = data.labels?.[index] || `'${year.slice(-2)}`;
      const values: Record<string, number> = {
        IBRD: data.ibrd[index] || 0,
        IDA: data.ida[index] || 0,
        'IBRD and IDA': data.ibrdAndIda?.[index] || 0,
      };

      return {
        id: year,
        label: shortLabel,
        values,
      };
    });
  }, [data]);

  return {
    data: mappedData,
    isLoading,
    errorMessage,
    series: disbursementSeries,
  };
};
