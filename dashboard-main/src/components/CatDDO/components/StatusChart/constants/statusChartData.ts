import type { StackedBarChartDataPoint, BarChartSeries } from '@/lib/BarChart';

export const statusChartData: StackedBarChartDataPoint[] = [
  { id: 'AFE', label: 'AFE', values: { Active: 4, Close: 4, Pipeline: 4 } },
  { id: 'AFW', label: 'AFW', values: { Active: 15, Close: 0, Pipeline: 0 } },
  { id: 'EAP', label: 'EAP', values: { Active: 0, Close: 0, Pipeline: 0 } },
  { id: 'ECA', label: 'ECA', values: { Active: 15, Close: 0, Pipeline: 0 } },
  { id: 'LCR', label: 'LCR', values: { Active: 0, Close: 0, Pipeline: 0 } },
  { id: 'MNA', label: 'MNA', values: { Active: 4, Close: 0, Pipeline: 2 } },
  { id: 'SAR', label: 'SAR', values: { Active: 6, Close: 0, Pipeline: 0 } },
];

export const statusSeries: BarChartSeries[] = [
  { key: 'Active', label: 'Active', color: '#a3c0e4' },
  { key: 'Closed', label: 'Closed', color: '#295e84' },
];
