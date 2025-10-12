import type { StackedBarChartDataPoint, BarChartSeries } from 'vizonomy';

export type RegionChartProps = object;

export interface RegionChartHookResult {
  data: StackedBarChartDataPoint[];
  isLoading: boolean;
  errorMessage: string;
  series: BarChartSeries[];
}
