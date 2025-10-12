import { useMemo } from 'react';
import type { StackedBarChartDataPoint, BarChartSeries } from '@/lib/BarChart';
import { statusSeries } from './constants/statusChartData';
import { useFetchRegionByStatus } from '@/hooks/useFetchRegionByStatus';

export const useStatusChart = () => {
  const { data, isLoading, errorMessage } = useFetchRegionByStatus();

  const seriesKeys = useMemo(
    () => statusSeries.map((s: BarChartSeries) => s.key as string),
    []
  );

  const mappedData = useMemo<StackedBarChartDataPoint[]>(() => {
    if (!data?.matrix?.length) return [];
    return data.matrix.map((row) => {
      const region = String((row as Record<string, unknown>).region ?? '');
      const values: Record<string, number> = {};
      seriesKeys.forEach((key) => {
        const rawValue = (row as Record<string, unknown>)[key] ?? 0;
        const numericValue = +rawValue;
        values[key] = Number.isFinite(numericValue) ? numericValue : 0;
      });
      return { id: region, label: region, values };
    });
  }, [data, seriesKeys]);

  return { data: mappedData, isLoading, errorMessage, series: statusSeries };
};
