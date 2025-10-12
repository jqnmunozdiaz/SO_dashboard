import type { StackedBarChartDataPoint, BarChartSeries } from 'vizonomy';

export type DisbursementChartProps = object;

export interface DisbursementChartHookResult {
  data: StackedBarChartDataPoint[];
  isLoading: boolean;
  errorMessage: string;
  series: BarChartSeries[];
}
