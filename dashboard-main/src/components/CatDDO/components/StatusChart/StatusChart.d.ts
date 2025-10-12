import type { StackedBarChartDataPoint, BarChartSeries } from 'vizonomy';

export type StatusChartProps = object;

export interface StatusChartHookResult {
  data: StackedBarChartDataPoint[];
  isLoading: boolean;
  errorMessage: string;
  series: BarChartSeries[];
}
