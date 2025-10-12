import { useMemo } from 'react';
import type { StackedBarChartDataPoint, BarChartSeries } from '@/lib/BarChart';
import { useFetchGlobalChart } from '@/hooks/useFetchGlobalChart';

export const useGlobalChart = () => {
  const { data, series, isLoading, error } = useFetchGlobalChart();

  const seriesKeys = useMemo(
    () => series.map((s: BarChartSeries) => s.key as string),
    [series]
  );

  const mappedData = useMemo<StackedBarChartDataPoint[]>(() => {
    if (!data?.length) return [];
    return data.map((row) => {
      const label = row.label ?? '';
      const values: Record<string, number> = {};
      seriesKeys.forEach((key) => {
        const rawValue = row.values[key] ?? 0;
        const numericValue = +rawValue;
        values[key] = Number.isFinite(numericValue) ? numericValue : 0;
      });
      return { id: row.id, label, values };
    });
  }, [data, seriesKeys]);

  return {
    data: mappedData,
    isLoading,
    errorMessage: error,
    series,
  };
};
