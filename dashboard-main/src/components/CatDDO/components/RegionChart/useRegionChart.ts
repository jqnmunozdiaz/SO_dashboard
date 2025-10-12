import { useMemo } from 'react';
import type { StackedBarChartDataPoint, BarChartSeries } from '@/lib/BarChart';
import { regionSeries } from './constants/regionChartData';
import { useFetchApprovalsByFiscalYearRegion } from '@/hooks/useFetchApprovalsByFiscalYearRegion';

export const useRegionChart = () => {
  const { data, isLoading, errorMessage } =
    useFetchApprovalsByFiscalYearRegion();

  const seriesKeys = useMemo(
    () => regionSeries.map((s: BarChartSeries) => s.key as string),
    []
  );

  const mappedData = useMemo<StackedBarChartDataPoint[]>(() => {
    if (!data?.matrix?.length) return [];
    return data.matrix.map((row) => {
      const year = String((row as Record<string, unknown>).year ?? '');
      const values: Record<string, number> = {};
      seriesKeys.forEach((key) => {
        const rawValue = (row as Record<string, unknown>)[key] ?? 0;
        const numericValue = +rawValue;
        values[key] = Number.isFinite(numericValue) ? numericValue : 0;
      });
      return { id: year, label: year, values };
    });
  }, [data, seriesKeys]);

  return { data: mappedData, isLoading, errorMessage, series: regionSeries };
};
