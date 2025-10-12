import { useMemo } from 'react';
import type { StackedBarChartDataPoint, BarChartSeries } from '@/lib/BarChart';
import { useFetchClimateCobenefits } from '@/hooks/useFetchClimateCobenefits';

export const useMixedDPOChart = () => {
  const { data, isLoading, error } = useFetchClimateCobenefits();

  const series = useMemo<BarChartSeries[]>(
    () => [
      {
        key: 'Adaptation co-benefits',
        label: 'Adaptation co-benefits',
        color: '#295e84',
      },
      {
        key: 'Mitigation co-benefits',
        label: 'Mitigation co-benefits',
        color: '#89A3C5',
      },
    ],
    []
  );

  const mappedData = useMemo<StackedBarChartDataPoint[]>(() => {
    if (!data?.mixed) return [];

    return data.mixed.labels.map((label, index) => {
      const values: Record<string, number> = {
        'Adaptation co-benefits': data.mixed.adapt[index] || 0,
        'Mitigation co-benefits': data.mixed.mitig[index] || 0,
      };

      return {
        id: label,
        label,
        values,
      };
    });
  }, [data]);

  return {
    data: mappedData,
    isLoading,
    errorMessage: error,
    series,
  };
};
